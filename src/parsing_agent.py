import glob
import os
from typing import List, Dict

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage, SystemMessage


class ParsingAgent:
    """
    Agent 1: PDF 文本提取与结构化摘要
    遍历 papers 目录下的所有 PDF，提取全文并让 LLM 总结出 Abstract、Method、Result 三大核心模块。
    """

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.max_text_length = 15000

    def process_papers(self, papers_dir: str) -> List[Dict[str, str]]:
        paper_summaries: List[Dict[str, str]] = []
        pdf_files = glob.glob(os.path.join(papers_dir, "*.pdf"))

        if not pdf_files:
            print("\u274c 未找到任何 PDF 文件，请将论文放入 papers 目录后重试。")
            return paper_summaries

        print(f"\U0001F4C4 解析 Agent 启动：共检测到 {len(pdf_files)} 篇 PDF 论文\n")

        system_prompt = SystemMessage(content=(
            "你是一个专业的学术文献解析助手。你的任务是从给定的英文论文全文中，精准提炼出三个核心模块。\n"
            "请严格按照以下 JSON 格式输出，不要添加任何其他内容：\n"
            '{{"abstract": "论文摘要与研究背景概述", "method": "核心方法与模型架构", "result": "主要实验数据与结论"}}\n'
            "要求使用中文输出，内容要详实、准确。"
        ))

        for idx, pdf_path in enumerate(pdf_files, start=1):
            filename = os.path.basename(pdf_path)
            print(f"\U0001F4D6 [{idx}/{len(pdf_files)}] 正在处理: {filename}")

            try:
                loader = PyPDFLoader(pdf_path)
                pages = loader.load()

                full_text = ""
                for page in pages:
                    full_text += page.page_content + "\n"

                if not full_text.strip():
                    print(f"    \u26A0\uFE0F 警告：未能从 {filename} 提取到文本内容，跳过。")
                    continue

                # 截断过长文本以防止超出模型上下文限制
                if len(full_text) > self.max_text_length:
                    full_text = full_text[:self.max_text_length]
                    print(f"    \U0001F4CF 文本过长已截断至 {self.max_text_length} 字符")

                human_prompt = HumanMessage(content=(
                    f"以下是论文《{filename}》的全文内容，请提炼 Abstract（摘要与研究背景）、Method（核心方法与模型）、Result（主要实验数据与结论）：\n\n"
                    f"{full_text}"
                ))

                response = self.llm.invoke([system_prompt, human_prompt])
                content = response.content.strip()

                # 解析 LLM 返回的 JSON
                import json
                try:
                    parsed = json.loads(content)
                except json.JSONDecodeError:
                    # 如果 LLM 输出非严格 JSON，尝试提取
                    import re
                    abstract_match = re.search(r'"abstract"\s*:\s*"([^"]*)"', content)
                    method_match = re.search(r'"method"\s*:\s*"([^"]*)"', content)
                    result_match = re.search(r'"result"\s*:\s*"([^"]*)"', content)
                    parsed = {
                        "abstract": abstract_match.group(1) if abstract_match else "未能提取",
                        "method": method_match.group(1) if method_match else "未能提取",
                        "result": result_match.group(1) if result_match else "未能提取",
                    }

                summary = {
                    "filename": filename,
                    "abstract": parsed.get("abstract", "未能提取"),
                    "method": parsed.get("method", "未能提取"),
                    "result": parsed.get("result", "未能提取"),
                }
                paper_summaries.append(summary)
                print(f"    \u2705 解析完成")

            except Exception as e:
                print(f"    \u274C 处理失败: {str(e)}")
                continue

        print(f"\n\u2705 解析 Agent 完成：成功解析 {len(paper_summaries)}/{len(pdf_files)} 篇论文\n")
        return paper_summaries
