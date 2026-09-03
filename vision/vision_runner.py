from vision_engine import run_vision_analysis


def start_vision():
    print("Starting Vision Analysis...")

    result = run_vision_analysis()

    return result


if __name__ == "__main__":
    start_vision()