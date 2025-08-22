# PNG-Card-Generator
Simple Python project for makeing basic png trading cards.

## How to use
Download the lastest relase and place it into its own folder. The file is unsigned so windows may give smart screen error when running for the first time.

### Default Config:
```
border_styles:
  Basic: [200, 200, 200, 80, 80, 80]
  Uncommon: [180, 255, 180, 0, 150, 0]
  Rare: [180, 200, 255, 0, 80, 200]
  Epic: [230, 200, 255, 100, 0, 100]
  Legendary: [255, 230, 180, 180, 100, 0]

gradient_types:
  Attack: [150, 0, 0, 255, 150, 150]
  Defense: [0, 0, 150, 150, 150, 255]
  Neutral: [80, 80, 80, 220, 220, 220]
  Bounty: [150, 120, 0, 255, 230, 150]

card_size:
  height: 900
  width: 600

border_width: 10
corner_radius: 25

font_file: "SpaceMono.ttf"
font_title: 40
font_desc: 28
```
Note: A new config is generated if none is found.
