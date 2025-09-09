import matplotlib.pyplot as plt
import unittest

from benchmark.ssh import BenchmarkSshHoneypot
from benchmark.test import BenchmarkTestRunner


def make_suite(model_name):
    suite = unittest.TestSuite()
    for method in unittest.TestLoader().getTestCaseNames(BenchmarkSshHoneypot):
        suite.addTest(BenchmarkSshHoneypot(model_name, method))
    return suite


def run_tests_for_model(model_name: str):
    runner = BenchmarkTestRunner(verbosity=2, model_name=model_name)
    return runner.run(make_suite(model_name))


if __name__ == '__main__':
    models = [
        'inception/mercury-coder',
        'openai/gpt-4o-2024-08-06',
        'sao10k/l3-lunaris-8b',
        'meta-llama/llama-3.2-1b-instruct',
        'mistralai/codestral-2508',
        'qwen/qwen3-30b-a3b-instruct-2507',
        'google/gemini-2.5-flash',
        'openai/gpt-4.1-mini',
        'x-ai/grok-code-fast-1',
        'deepseek/deepseek-chat-v3-0324',
    ]
    results = {}
    pass_rates = []
    times = []

    for model_name in models:
        print('running', model_name)
        runner = BenchmarkTestRunner(verbosity=2, model_name=model_name)
        result = runner.run(make_suite(model_name))
        results[model_name] = result.metrics

    # final combined report
    with open('result.txt', 'w') as f:
        f.write('\n=== Combined Benchmark Report ===\n')
        for model, m in results.items():
            pass_rates.append(m['pass_rate'])
            times.append(m['elapsed_time'])
            f.write(f'{model}: {m['pass_rate']:.2f}% pass rate '
                  f'({m['passed']}/{m['total']} tests) in {m['elapsed_time']:.2f}s\n')

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot pass rate on left y-axis
    ax1.plot(models, pass_rates, marker="o", color="tab:blue", label="Pass Rate (%)")
    ax1.set_ylabel("Pass Rate (%)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xticklabels(models, rotation=45, ha="right")

    # Plot elapsed time on right y-axis
    ax2 = ax1.twinx()
    ax2.plot(models, times, marker="s", color="tab:red", label="Elapsed Time (s)")
    ax2.set_ylabel("Elapsed Time (s)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    # Title and grid
    plt.title("Model Benchmark: Pass Rate vs Time")
    fig.tight_layout()
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)

    plt.show()
