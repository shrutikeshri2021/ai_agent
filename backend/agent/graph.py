from agent.parser import parse_instruction
from agent.generator import generate_playwright_steps
from agent.executor import run_test
from agent.reporter import generate_pdf_report, generate_report

def run_agent(user_input):
    parsed = parse_instruction(user_input)
    steps = generate_playwright_steps(parsed)
    results, logs = run_test(steps)
    report = generate_report(results, logs)
    generate_pdf_report(report)

    return report
