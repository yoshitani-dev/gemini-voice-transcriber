import wave
import math
import os
import sys

def split_wav_by_duration(input_file, output_prefix, split_duration_sec):
    """
    WAVファイルを指定した秒数ごとに分割する関数
    """
    try:
        # 出力用の保存フォルダ名（例: sample_splits）
        output_dir = f"{output_prefix}_splits"
        # フォルダが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)
        abs_output_dir = os.path.abspath(output_dir)

        with wave.open(input_file, 'rb') as infile:
            # 音声のパラメータを取得
            nchannels = infile.getnchannels()
            sampwidth = infile.getsampwidth()
            framerate = infile.getframerate()
            nframes = infile.getnframes()
            comptype = infile.getcomptype()
            compname = infile.getcompname()

            # 合計の秒数を計算
            total_duration_sec = nframes / float(framerate)
            
            # 1分割あたりのフレーム数を計算
            frames_per_split = int(framerate * split_duration_sec)
            
            # 分割されるファイルの総数を計算
            num_splits = math.ceil(nframes / frames_per_split)
            
            print("\n--- 分割処理を開始します ---")
            print(f"入力ファイル     : {os.path.abspath(input_file)}")
            print(f"保存先フォルダ   : {abs_output_dir}")
            print(f"サンプリングレート: {framerate} Hz")
            print(f"チャンネル数     : {nchannels}")
            print(f"合計時間         : {total_duration_sec / 60:.2f} 分 ({total_duration_sec:.2f} 秒)")
            print(f"分割単位         : {split_duration_sec / 60:.2f} 分 ({split_duration_sec} 秒)")
            print(f"作成ファイル数   : {num_splits} 個")
            print("-" * 40)

            for i in range(num_splits):
                # 書き出すファイル名を作成（連番をつける）
                filename = f"{output_prefix}_{i+1:03d}.wav"
                output_filepath = os.path.join(output_dir, filename)
                
                # 読み込むフレーム数を計算（最後は余りのフレーム）
                frames_to_read = min(frames_per_split, nframes - (i * frames_per_split))
                
                # データを読み込む
                data = infile.readframes(frames_to_read)
                
                # 新しいWAVファイルとして書き出す
                with wave.open(output_filepath, 'wb') as outfile:
                    outfile.setnchannels(nchannels)
                    outfile.setsampwidth(sampwidth)
                    outfile.setframerate(framerate)
                    outfile.setnframes(frames_to_read)
                    outfile.setcomptype(comptype, compname)
                    outfile.writeframes(data)
                
                print(f"【保存完了】 {filename}")
                
        print("-" * 40)
        print("すべての分割処理が完了しました！")
        print(f"保存フォルダを開く: {abs_output_dir}")
        
    except wave.Error as e:
        print(f"WAVファイルの処理中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

def select_wav_file():
    """
    実行フォルダ内のWAVファイルを検索し、ユーザーに選択させる関数
    """
    # カレントディレクトリにある.wavファイル一覧を取得
    wav_files = [f for f in os.listdir('.') if f.lower().endswith('.wav') and os.path.isfile(f)]
    
    if not wav_files:
        print("\n[エラー] このフォルダ内にWAVファイルが見つかりません。")
        print("分割したいWAVファイルを、このスクリプトと同じフォルダに置いてから実行してください。")
        input("\nEnterキーを押すと終了します...")
        sys.exit(1)
        
    if len(wav_files) == 1:
        selected_file = wav_files[0]
        print(f"\nWAVファイルが見つかりました: {selected_file}")
        return selected_file
        
    print("\nフォルダ内に複数のWAVファイルが見つかりました。")
    print("分割したいファイルの番号を入力してEnterを押してください：")
    for idx, f in enumerate(wav_files, 1):
        print(f"  [{idx}] {f}")
        
    while True:
        try:
            choice = input(f"選択 (1-{len(wav_files)}, デフォルト: 1): ").strip()
            # 未入力（Enterのみ）の場合は1番を選択
            if choice == "":
                selected_file = wav_files[0]
                print(f"-> 「{selected_file}」を選択しました。")
                return selected_file
            
            idx = int(choice)
            if 1 <= idx <= len(wav_files):
                selected_file = wav_files[idx-1]
                print(f"-> 「{selected_file}」を選択しました。")
                return selected_file
            else:
                print(f"1から{len(wav_files)}の範囲で入力してください。")
        except ValueError:
            print("有効な数値を入力してください。")

def get_duration_input():
    """
    分割する時間をユーザーに入力させる関数
    """
    while True:
        try:
            duration_min_str = input("\n何分ごとに分割しますか？ (デフォルト: 5分): ").strip()
            if duration_min_str == "":
                return 5 * 60  # デフォルト5分 (300秒)
            
            duration_min = float(duration_min_str)
            if duration_min <= 0:
                print("0より大きい数値を入力してください。")
                continue
            return int(duration_min * 60)
        except ValueError:
            print("数値を入力してください（例: 5 や 2.5 など）。")

if __name__ == "__main__":
    print("=" * 45)
    print("         WAVファイル自動分割ツール")
    print("=" * 45)
    
    # ヘルプ表示の対応
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("使い方:")
        print("  【引数を指定して非対話実行（ターミナル用）】")
        print("    python split_wav.py <WAVファイル名> [分割時間(秒)] [出力接頭辞]")
        print("    例: python split_wav.py sample.wav 300 my_split")
        print("\n  【引数なしで対話実行】")
        print("    python split_wav.py")
        sys.exit(0)

    # コマンドライン引数が渡された場合（ターミナルからの直接実行）
    if len(sys.argv) > 1:
        input_wav = sys.argv[1]
        
        # 分割時間（秒）の取得。デフォルトは300秒（5分）
        duration_sec = 300
        if len(sys.argv) > 2:
            try:
                duration_sec = int(sys.argv[2])
            except ValueError:
                print(f"警告: 分割時間 '{sys.argv[2]}' が無効です。デフォルトの300秒を使用します。")
                
        # 出力プレフィックスの取得。デフォルトは「ファイル名_split」
        default_prefix = os.path.splitext(input_wav)[0] + "_split"
        output_base = sys.argv[3] if len(sys.argv) > 3 else default_prefix
        
        if not os.path.exists(input_wav):
            print(f"[エラー] 指定されたファイル '{input_wav}' が見つかりません。")
            sys.exit(1)
            
        # 分割処理を実行
        split_wav_by_duration(input_wav, output_base, duration_sec)
        
    # 引数がない場合は対話（インタラクティブ）モードで実行
    else:
        # 1. 自動でWAVファイルを探して選択させる
        input_wav = select_wav_file()
        
        # 2. 分割する時間を入力させる（デフォルトは5分）
        duration_sec = get_duration_input()
        
        # 3. 出力ファイル名の接頭辞を入力させる
        default_prefix = os.path.splitext(input_wav)[0] + "_split"
        output_base = input(f"\n出力ファイルの名前（接頭辞）を入力してください\n(空白のままEnterを押すと「{default_prefix}」になります): ").strip()
        if output_base == "":
            output_base = default_prefix
            
        # 分割処理を実行
        split_wav_by_duration(input_wav, output_base, duration_sec)
        
        # ダブルクリック実行時の自動終了を防ぐ
        input("\nEnterキーを押して終了します...")
