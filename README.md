# Energy atmospheric rivers - Victoire Buffet et al
An energy atmospheric rivers (AR) detection algorithm for global studies. The algorithm is following the method of Wille et al. (2021) vIVT and IWV atmospheric river detection algorithm, implemented in python. It is applied to latent heat (LH) on one hand and sensible heat (SH) on the other hand, either based on their vertically integrated meridional transport (vLHT and vSHT) --which is analogous to Wille et al (2021) vIVT scheme-- or their vertically integrated value (ILH and ISH), which is analogous to Wille et al (2021) IWV scheme. 

This code will be subject to amendment and improvement over time.

If you use or adapt this python script please acknowledge the source, and reference the GitHub repository at:
https://github.com/victoirebuffet/energy_atmospheric_rivers/

## Detection algorithm

## Running the algorithm

1 - Generate the config file according to your needs :
```
python generate_config.py
```
2 - Run the main script :
```
 python main.py config.json
```
