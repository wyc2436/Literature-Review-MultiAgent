from typing import List, Dict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class ReasoningAgent:
    """
    Agent 2: 跨文献推理与 Research Gap 分析
    将所有论文的结构化摘要拼接后，让 LLM 扮演资深学术博导进行横向对比和 Gap 分析。
    """

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def analyze_gaps(self, topic: str, paper_summaries: List[Dict[str, str]]) -> str:
        if not paper_summaries:
            return "⚠️ 没有可用的论文摘要，无法进行推理分析。"

        print(f"\U0001F9E0 推理 Agent 启动：正在对 {len(paper_summaries)} 篇论文进行横向对比分析\n")

        # 构建拼接上下文
        combined_summaries = f"研究主题：{topic}\n\n"
        for idx, paper in enumerate(paper_summaries, start=1):
            combined_summaries += (
                f"━━━ 论文 {idx}：{paper.get('filename', '未知')} ━━━\n"
                f"【摘要与研究背景】\n{paper.get('abstract', 'N/A')}\n\n"
                f"【核心方法与模型】\n{paper.get('method', 'N/A')}\n\n"
                f"【主要实验数据与结论】\n{paper.get('result', 'N/A')}\n\n"
            )

        system_prompt = SystemMessage(content=(
            "你是一位资深学术博导，拥有20年以上的科研指导经验，擅长跨文献横向对比与发现研究空白（Research Gap）。\n\n"
            "请根据提供的一系列论文的结构化摘要，完成以下分析：\n\n"
            "1. **研究共识总结**：这些论文在该研究主题上达成了哪些共识？\n"
            "2. **核心方法对比**：各论文采用了哪些不同的技术路线和方法？各自的优劣是什么？\n"
            "3. **实验结果横向对比**：各论文的实验设置和核心指标对比如何？\n"
            "4. **核心创新点梳理**：每篇论文的独特贡献和创新之处。\n"
            "5. **Research Gap 分析**（重点）：当前研究中存在的空白、未解决的问题、相互矛盾的结论，"
            "以及未来值得探索的研究方向。请给出至少 3 个具体的 Research Gap。\n\n"
            "要求：输出使用中文，条理清晰，分析深入，每个部分至少 200 字。"
        ))

        human_prompt = HumanMessage(content=(
            f"请对以下与「{topic}」相关的论文进行深度横向对比分析，重点挖掘 Research Gap：\n\n"
            f"{combined_summaries}"
        ))

        print("    \U0001F4AC 正在向大模型发送推理请求...")
        response = self.llm.invoke([system_prompt, human_prompt])
        gap_analysis = response.content.strip()

        print(f"    \u2705 推理分析完成（共 {len(gap_analysis)} 字符）\n")
        return gap_analysis
