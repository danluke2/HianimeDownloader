import argparse
import json
import os
import time

from colorama import Fore

from extractors.general import GeneralExtractor
from extractors.hianime import HianimeExtractor
from extractors.instagram import InstagramExtractor


class Main:
    def __init__(self):
        self.args = self.parse_args()
        extractor = self.get_extractor()
        extractor.run()

    def get_extractor(self):
        if not self.args.link and not self.args.filename:
            os.system("cls" if os.name == "nt" else "clear")
            ans = input(
                f"{Fore.LIGHTGREEN_EX}GDown {Fore.LIGHTCYAN_EX}Downloader\n\nProvide a link or search for an anime:\n{Fore.LIGHTYELLOW_EX}"
            )
            if "http" in ans.lower():
                self.args.link = ans
            else:
                return HianimeExtractor(args=self.args, name=ans)

        if not self.args.link and self.args.filename:
            return HianimeExtractor(args=self.args, name=self.args.filename)

        if "hianime" in self.args.link:
            return HianimeExtractor(args=self.args)
        if "instagram.com" in self.args.link:
            return InstagramExtractor(args=self.args)
        return GeneralExtractor(args=self.args)

    def load_config(self):
        """Load configuration from config.json file if it exists, otherwise use config.default.json."""
        config_dir = os.path.dirname(__file__)
        config = {}
        
        # Try to load user's personal config first
        config_path = os.path.join(config_dir, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"{Fore.LIGHTYELLOW_EX}Warning: Could not load config.json: {e}")
        
        # Fall back to default config if personal config not loaded
        if not config:
            default_config_path = os.path.join(config_dir, "config.default.json")
            if os.path.exists(default_config_path):
                try:
                    with open(default_config_path, "r") as f:
                        config = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"{Fore.LIGHTYELLOW_EX}Warning: Could not load config.default.json: {e}")
        
        return config

    def parse_args(self):
        # Load defaults from config file
        config = self.load_config()
        
        # Determine output directory based on content type
        if config.get("is_movie", False):
            output_dir = config.get("movie_output_dir", "movies")
        elif config.get("is_ova", False):
            output_dir = config.get("ova_output_dir", "OVAs")
        else:
            output_dir = config.get("output_dir", "output")
        
        parser = argparse.ArgumentParser(description="Anime downloader options")

        parser.add_argument(
            "--subtitles",
            action="store_true",
            default=config.get("subtitles", True),
            help="Download subtitle files (.vtt or .srt)",
        )

        parser.add_argument(
            "-o",
            "--output-dir",
            type=str,
            default=output_dir,
            help="Directory to save downloaded files",
        )

        parser.add_argument(
            "-n",
            "--filename",
            type=str,
            default=config.get("filename", ""),
            help="Used for name of anime, or name of output file when using other extractor",
        )

        parser.add_argument(
            "--aria",
            action="store_true",
            default=config.get("aria", False),
            help="Use aria2c as external downloader",
        )

        parser.add_argument(
            "-l",
            "--link",
            type=str,
            default=config.get("link", None),
            help="Provide link to desired content",
        )

        parser.add_argument(
            "--server", 
            type=str, 
            default=config.get("server", None), 
            help="Streaming Server to download from"
        )

        parser.add_argument(
            "--default-server", 
            type=str, 
            default=config.get("default_server", None), 
            help="Default streaming server to use if no --server is provided"
        )

        parser.add_argument(
            "--default-download-type", 
            type=str, 
            default=config.get("default_download_type", None), 
            help="Default download type (sub or dub) to use if both are available"
        )

        parser.add_argument(
            "--max-retries", 
            type=int, 
            default=config.get("max_retries", 60), 
            help="Max retries to find url"
        )

        parser.add_argument(
            "--json-file", 
            type=str, 
            default=config.get("json_file", None), 
            help="Path to a JSON file with episode data"
        )

        parser.add_argument(
            "--is-movie",  
            action="store_true", 
            default=config.get("is_movie", False), 
            help="Searching for a movie"
        )

        parser.add_argument(
            "--is-ova",  
            action="store_true", 
            default=config.get("is_ova", False), 
            help="Searching for an OVA"
        )

        parser.add_argument(
            "--srt-format",  
            action="store_true", 
            default=config.get("srt_format", False), 
            help="Convert subtitle files to SRT format instead of VTT"
        )

        return parser.parse_args()


if __name__ == "__main__":
    start = time.time()
    Main()
    elapsed = time.time() - start
    print(f"Took {int(elapsed / 60)}:{int((elapsed % 60))} to finish")
