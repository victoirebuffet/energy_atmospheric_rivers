# Energy atmospheric rivers - Victoire Buffet *et al.*
An energy atmospheric rivers (AR) detection algorithm for global studies. The algorithm is following the method of Wille *et al.* (2021) vIVT and IWV atmospheric river detection algorithm, implemented in python. It is applied to latent heat (LH) on one hand and sensible heat (SH) on the other hand, either based on their vertically integrated meridional transport (v**LH**T and v**SH**T) —which is analogous to Wille *et al.* (2021) vIVT scheme— or their vertically integrated value (I**LH** and I**SH**), which is analogous to Wille *et al.* (2021) IWV scheme. 

This code might be subject to amendment and improvement over time.

If you use or adapt this python script please acknowledge the source, and reference the GitHub repository at:
https://github.com/victoirebuffet/energy_atmospheric_rivers/

## Detection algorithm

## Running the algorithm

Run this algorithm in two steps : 

1 - If you wish to create the json config file using a python script, modify the ```
 write_config.py
``` script according to your needs  and then execute this : 
```
python write_config.py
```
You can skip this step by just creating a .json config file with a text editor, in a similar way as the one provided in the main branch.

2 - Run the main script :
```
 python main.py config.json
```
