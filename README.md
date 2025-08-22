# PNG-Card-Generator
Simple Python project for makeing basic png trading cards.

## How to use
[Download the lastest release](https://github.com/Glitched-Reality/PNG-Card-Generator/releases/latest) and place it into its own folder. The file is unsigned so windows may give smart screen error when running for the first time.

### Default Config:
```
border_styles:
  Basic:
  - 150
  - 150
  - 150
  - 100
  - 100
  - 100
  Uncommon:
  - 180
  - 255
  - 180
  - 0
  - 150
  - 0
  Rare:
  - 180
  - 200
  - 255
  - 0
  - 80
  - 200
  Epic:
  - 230
  - 200
  - 255
  - 100
  - 0
  - 100
  Legendary:
  - 255
  - 230
  - 180
  - 180
  - 100
  - 0
gradient_types:
  Attack:
  - 180
  - 60
  - 60
  - 220
  - 100
  - 100
  Defense:
  - 60
  - 60
  - 180
  - 120
  - 120
  - 220
  Neutral:
  - 120
  - 120
  - 120
  - 180
  - 180
  - 180
  Bounty:
  - 180
  - 150
  - 80
  - 220
  - 190
  - 120
card_size:
  height: 900
  width: 600
border_width: 10
corner_radius: 25
font_file: C:/Windows/Fonts/arial.ttf
font_title: 40
font_desc: 28
```
Note: A new config is generated if none is found.
