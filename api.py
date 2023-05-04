import inspect
from termcolor import colored

from steamship import check_environment, RuntimeEnvironments, Steamship
from steamship.invocable import post, PackageService


class PromptPackage(PackageService):
    PROMPT = "Generate a simple web development project idea that can be completed in a day:"

    @post("generate")
    def generate(self) -> str:
        """Generate a web development project idea."""
        llm_config = {
            "max_words": 30,
            "temperature": 0.8
        }

        llm = self.client.use_plugin("gpt-3", config=llm_config)
        return llm.generate(self.PROMPT)


def generate_project_idea(prompt: PromptPackage) -> None:
    print(colored("Generating...", 'green'))
    print(colored("Project Idea:", 'green'), f'{prompt.generate()}\n')


def main():
    print(colored("Generate web development project ideas with GPT-3\n", attrs=['bold']))

    check_environment(RuntimeEnvironments.REPLIT)

    with Steamship.temporary_workspace() as client:
        prompt = PromptPackage(client)

        print(colored("Here is a web development project idea", 'green'))
        generate_project_idea(prompt)

        try_again = True
        while try_again:
            try_again = input(colored("Generate another (y/n)? ", 'green')).lower().strip() == 'y'
            if try_again:
                generate_project_idea(prompt)
            print()

        print("Ready to share with your friends (and the world)?\n")
        print(" 1. Run: echo steamship >> requirements.txt")
        print(" 2. Run: echo termcolor >> requirements.txt")
        print(" 3. Run: ship deploy")
        print("\n.. to get a production-ready API and a web-based demo app.\n")


if __name__ == "__main__":
    main()
