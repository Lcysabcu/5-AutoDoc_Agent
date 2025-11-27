import subprocess
from shutil import rmtree
from typing import List
from pathlib import Path
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from utils import remove_readonly
from crew import initialize_planning_crew, initialize_documentation_crew

class DocumentationState(BaseModel):
    """
    文档流程的状态
    """
    project_url: str = ""
    repo_path: Path = "workdir"
    docs: List[str] = []

class CreateDocumentationFlow(Flow[DocumentationState]):
    # 克隆仓库，初始步骤
    @start()
    def clone_repo(self):
        print(f"# 正在克隆仓库: {self.state.project_url}\n")
        # 从 URL 提取仓库名称
        repo_name = self.state.project_url.split("/")[-1]
        self.state.repo_path = f"{self.state.repo_path}/{repo_name}"

        # 检查目录是否存在
        if Path(self.state.repo_path).exists():
            print(f"# 仓库目录已存在于 {self.state.repo_path}\n")
            # subprocess.run(["rm", "-rf", self.state.repo_path])
            rmtree(self.state.repo_path, onexc=remove_readonly)
            print("# 已移除现有目录\n")

        # 克隆仓库
        subprocess.run(["git", "clone", self.state.project_url, self.state.repo_path], check=True)
        return self.state

    @listen(clone_repo)
    def plan_docs(self):
        print(f"# 正在为 {self.state.repo_path} 规划文档\n")
        planning_crew = initialize_planning_crew()
        result = planning_crew.kickoff(inputs={'repo_path': self.state.repo_path})
        print(f"# 已为 {self.state.repo_path} 规划文档:")
        for doc in result.pydantic.docs:
            print(f"    - {doc.title}")
        return result

    @listen(plan_docs)
    def save_plan(self, plan):
        docs_dir = Path("docs")
        if docs_dir.exists():
            rmtree(docs_dir, onexc=remove_readonly)
        docs_dir.mkdir(exist_ok=True)
        with open(docs_dir / "plan.json", "w") as f:
            f.write(plan.raw)
        print("# 文档计划已保存到 docs/plan.json")

    @listen(plan_docs)
    def create_docs(self, plan):
        for doc in plan.pydantic.docs:
            print(f"\n# 正在为 {doc.title} 创建文档")
            documentation_crew = initialize_documentation_crew()
            result = documentation_crew.kickoff(inputs={
                'repo_path': self.state.repo_path,
                'title': doc.title,
                'overview': plan.pydantic.overview,
                'description': doc.description,
                'prerequisites': doc.prerequisites,
                'examples': '\n'.join(doc.examples),
                'goal': doc.goal
            })

            # 将文档保存到 docs 文件夹中的文件
            docs_dir = Path("docs")
            docs_dir.mkdir(exist_ok=True)
            title = doc.title.lower().replace(" ", "_") + ".mdx"
            self.state.docs.append(str(docs_dir / title))
            with open(docs_dir / title, "w") as f:
                f.write(result.raw)
            print(f"# 已保存文档: docs/{title}")
        
        print(f"\n# 已完成 {self.state.repo_path} 的文档创建")
        print(f"# 共生成 {len(self.state.docs)} 个文档文件")
        return self.state.docs