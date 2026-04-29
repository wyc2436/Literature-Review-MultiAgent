import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.parsing_agent import ParsingAgent
from src.reasoning_agent import ReasoningAgent
from src.writing_agent import WritingAgent

# 加载环境变量
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


def print_banner():
    """打印项目启动横幅"""
    banner = r"""
╔══════════════════════════════════════════════════════════════╗
║         多 Agent 文献精读与综述生成系统                       ║
║         Multi-Agent Literature Review System                ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_environment():
    """检查环境配置"""
    if not DEEPSEEK_API_KEY:
        print("\u274C 错误：未配置 DEEPSEEK_API_KEY 环境变量！")
        print("   请复制 .env.example 为 .env 并填入您的 DeepSeek API Key。")
        sys.exit(1)
    print(f"\u2705 环境变量已加载")
    print(f"   Base URL: {DEEPSEEK_BASE_URL}")
    print(f"   API Key : {'*' * 20}{DEEPSEEK_API_KEY[-4:] if len(DEEPSEEK_API_KEY) >= 4 else '****'}")


def check_papers_directory(papers_dir: str):
    """检查论文目录是否存在且包含 PDF"""
    if not os.path.exists(papers_dir):
        os.makedirs(papers_dir)
        print(f"\U0001F4C1 已创建论文目录：{papers_dir}/")
        print("\u26A0\uFE0F  请将需要分析的 PDF 论文放入该目录后重新运行程序。")
        sys.exit(0)

    pdf_count = sum(1 for f in os.listdir(papers_dir) if f.lower().endswith(".pdf"))
    if pdf_count == 0:
        print(f"\U0001F4C1 论文目录：{papers_dir}/")
        print("\u26A0\uFE0F  该目录中没有 PDF 文件，请放入论文后重新运行程序。")
        sys.exit(0)

    print(f"\U0001F4C1 论文目录检测完成：发现 {pdf_count} 篇 PDF")


def main():
    print_banner()

    # 1. 检查环境配置
    print("\n" + "=" * 60)
    print("  \U0001F50D Phase 1: 环境检查")
    print("=" * 60)
    check_environment()

    # 2. 检查论文目录
    print("\n" + "=" * 60)
    print("  \U0001F4C4 Phase 2: 论文目录检查")
    print("=" * 60)
    papers_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "papers")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    check_papers_directory(papers_dir)

    # 3. 获取研究主题
    print("\n" + "=" * 60)
    print("  \U0001F4AC Phase 3: 研究主题确认")
    print("=" * 60)
    print("请输入您的研究主题（例如：大语言模型的多模态能力、自动驾驶中的目标检测等）：")
    research_topic = input("   >>> 研究主题: ").strip()
    while not research_topic:
        print("   \u26A0\uFE0F  研究主题不能为空，请重新输入：")
        research_topic = input("   >>> 研究主题: ").strip()
    print(f"   \u2705 研究主题: {research_topic}")

    # 4. 初始化 LLM
    print("\n" + "=" * 60)
    print("  \U0001F916 Phase 4: 初始化大语言模型")
    print("=" * 60)
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base=DEEPSEEK_BASE_URL.rstrip("/"),
        temperature=0.3,
        max_tokens=8192,
    )
    print(f"   \u2705 LLM 初始化完成：deepseek-chat")

    # 生成输出文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"literature_review_{timestamp}.md"
    output_path = os.path.join(output_dir, output_filename)

    # 5. Agent 1: 解析 Agent
    print("\n" + "=" * 60)
    print("  \U0001F4D6 Phase 5: 解析 Agent 工作中")
    print("=" * 60)
    parsing_agent = ParsingAgent(llm)
    paper_summaries = parsing_agent.process_papers(papers_dir)

    if not paper_summaries:
        print("\u274C 解析失败：未能从任何 PDF 中提取有效内容，程序终止。")
        sys.exit(1)

    # 6. Agent 2: 推理 Agent
    print("\n" + "=" * 60)
    print("  \U0001F9E0 Phase 6: 推理 Agent 工作中")
    print("=" * 60)
    reasoning_agent = ReasoningAgent(llm)
    gap_analysis = reasoning_agent.analyze_gaps(research_topic, paper_summaries)

    # 7. Agent 3: 撰写 Agent
    print("\n" + "=" * 60)
    print("  \U0001F4DD Phase 7: 撰写 Agent 工作中")
    print("=" * 60)
    writing_agent = WritingAgent(llm)
    writing_agent.generate_review(research_topic, paper_summaries, gap_analysis, output_path)

    # 8. 完成
    print("\n" + "=" * 60)
    print("  \U0001F389 全部流程完成！\U0001F389")
    print("=" * 60)
    print(f"\U0001F4C4 综述文件：output/{output_filename}")
    print(f"\U0001F4CA 解析论文数：{len(paper_summaries)} 篇")
    print(f"\U0001F4DD 综述字符数：见输出文件")
    print("\n感谢使用多 Agent 文献精读与综述生成系统！\n")


if __name__ == "__main__":
    main()
