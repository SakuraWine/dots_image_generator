# dots image generator

画像ファイルから点字で描かれた画像を出力する。

## Install

```bash
git clone https://github.com/SakuraWine/dots_image_generator.git
cd dots_image_generator
pip install -r requirements.txt
```

## Usage

```bash
python ./src/converter.py -s <path_to_source> -l <level>
```

## Args

- -s [--source-image] 元画像のパス
- -l [--level] 難易度（大きいほど低い解像度の画像が出力される）


## Example

```bash
python ./src/converter.py -s sample.png -l 5
```
