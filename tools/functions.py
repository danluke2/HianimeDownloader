import os
import time
import webvtt


def vtt_to_srt(vtt_file: str, srt_file: str | None = None) -> str:
    """
    Convert a VTT subtitle file to SRT format.
    
    Args:
        vtt_file: Path to the input VTT file
        srt_file: Path to the output SRT file (optional, defaults to same name with .srt extension)
    
    Returns:
        Path to the created SRT file
    """
    if srt_file is None:
        srt_file = os.path.splitext(vtt_file)[0] + ".srt"
    
    # Read VTT file
    vtt = webvtt.read(vtt_file)
    
    # Convert to SRT format
    srt_lines = []
    for i, caption in enumerate(vtt, start=1):
        # Add sequence number
        srt_lines.append(str(i))
        
        # Convert timestamp format from 00:00:00.000 to 00:00:00,000
        start_time = caption.start.replace(".", ",")
        end_time = caption.end.replace(".", ",")
        srt_lines.append(f"{start_time} --> {end_time}")
        
        # Add caption text (webvtt already handles cleaning tags)
        srt_lines.append(caption.text)
        
        # Add blank line between captions
        srt_lines.append("")
    
    # Write SRT file
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
    
    return srt_file


def get_confirmation(prompt: str) -> bool:
    ans: str = input(prompt).lower()
    if ans == "y" or ans == "yes" or ans == "true":
        return True
    elif ans == "n" or ans == "no" or ans == "false":
        return False
    else:
        print("Please provide a valid response")
        return get_confirmation(prompt)


def get_int_in_range(
    prompt: str, _min: int = 0, _max: int | float = float("inf"), default: int | None = None
) -> int:
    ans: str = input(prompt)
    if ans.strip() == "" and default is not None:
        return default
    try:
        _int: int = int(ans)
    except ValueError:
        print("Invalid input. Please provide a valid number.")
        return get_int_in_range(prompt, _min, _max)

    if _min <= _int <= _max:
        return _int

    print("Invalid input. The provide input was not within the expected range.")
    return get_int_in_range(prompt, _min, _max, default)


def safe_remove(file: str, retries: int = 5, delay: int = 2):
    for _ in range(retries):
        try:
            if os.path.exists(file):
                os.remove(file)
                return
            print("No file exists")
            return
        except PermissionError:
            print("Retrying deletion of files")
            time.sleep(delay)
    print("failed to remove file")
