import os
import time
import sys

import user_input
import timestp

from faster_whisper import WhisperModel
from faster_whisper.utils import download_model
from pathlib import Path

file_name = user_input.ask_file_name()

script_dir = Path(__file__).parent
project_root = script_dir.parent

video_path = project_root / "videos"
txt_path = project_root / "text"

video_file = video_path / f"{file_name}.mp4"
output_txt_file = txt_path / f"{file_name}.txt"
output_srt_file = video_path / f"{file_name}.srt"

if not os.path.exists(video_file):
    print(f"Ошибка: Файл '{video_file}' не найден в текущей папке!")
    print("Положите аудиофайл рядом со скриптом или укажите правильный путь.")
    sys.exit(1)

model_name = user_input.ask_model()

model_path = download_model(model_name)

print(
    "Загрузка модели Whisper... Это может занять некоторое время при первом запуске."
)
model = WhisperModel(model_path, device="cpu", compute_type="int8")

print(f"Начинаю расшифровку файла: {video_file}")
start_time = time.time()

# Распознавание речи
print("Идет распознавание речи (это может занять время)...")
segments, info = model.transcribe(
    video_file,
    language="ru",
    beam_size=5,
    vad_filter=True,  # <-- Ключевое улучшение для лекций
    vad_parameters=dict(
        min_silence_duration_ms=500)  # Игнорирует паузы короче 0.5 сек
)

print(
    f"Обнаружен язык: {info.language} (с вероятностью {info.language_probability:.2f})"
)
print("Запись результата в файлы...")

# Одновременная запись в TXT и SRT за один проход по сегментам
with open(output_txt_file, "w", encoding="utf-8") as txt_f, \
     open(output_srt_file, "w", encoding="utf-8") as srt_f:

    for i, segment in enumerate(segments, start=1):
        clean_text = segment.text.strip()

        # --- Запись в TXT файл ---
        txt_timestamp = timestp.format_txt_timestamp(segment.start)
        txt_line = f"{txt_timestamp} {clean_text}\n"
        txt_f.write(txt_line)
        print(txt_line, end="")  # Вывод в консоль для отслеживания

        # --- Запись в SRT файл ---
        srt_start = timestp.format_srt_timestamp(segment.start)
        srt_end = timestp.format_srt_timestamp(segment.end)

        srt_f.write(f"{i}\n")
        srt_f.write(f"{srt_start} --> {srt_end}\n")
        srt_f.write(f"{clean_text}\n\n")

end_time = time.time()
print(f"\nГотово! Текст успешно сохранен в: {output_txt_file}")
print(f"Субтитры успешно сохранены в: {output_srt_file}")
print(f"Время выполнения: {int(end_time - start_time)} сек.")
