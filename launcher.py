if __name__ == "__main__":
    import os
    import argparse

    from dotenv import load_dotenv
    from bot import CeresBot

    if os.path.exists(".env.dev"):
        load_dotenv(".env.dev")
    else:
        load_dotenv(".env")

    parser = argparse.ArgumentParser(description="Ceres bot launcher.")
    parser.add_argument("--join", action="store_true", default=False, help="Displays a link to add the bot to a discord guild.")

    args = parser.parse_args()

    def launch():
        if args.join:
            app_id = os.getenv("BOT_APP_ID", "APP_ID_MISSING")
            print(f"https://discord.com/oauth2/authorize?client_id={app_id}&scope=bot&permissions=8")
            return

        c_bot = CeresBot()
        CeresBot.run(c_bot)

        return

    launch()
