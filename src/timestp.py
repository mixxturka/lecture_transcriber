import datetime


def format_txt_timestamp(seconds: float) -> str:
    """Return a literal timestamp in format: [hh:mm:ss] for .txt file 
    
    1. seconds: time in seconds which needs to be converted in another format
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"


def format_srt_timestamp(seconds: float) -> str:
    """Return a literal timestamp in format: hh:mm:ss,mmm for .srt file 
        
    1. seconds: time in seconds which needs to be converted in another format
    """
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
