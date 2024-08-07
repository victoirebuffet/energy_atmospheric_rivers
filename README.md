# Energy Atmospheric Rivers - V. Buffet supervised by B. Pohl, V. Favier (M2 internship)

An energy atmospheric rivers (AR) detection algorithm for global studies. The algorithm follows the method of Wille *et al.* (2021) vIVT and IWV atmospheric river detection algorithm, implemented in Python. It is applied to latent heat (LH) on one hand and sensible heat (SH) on the other hand, either based on their vertically integrated meridional transport (v**LH**T and v**SH**T) — which is analogous to Wille *et al.* (2021) vIVT scheme — or their vertically integrated value (I**LH** and I**SH**), which is analogous to Wille *et al.* (2021) IWV scheme.

This code might be subject to amendment and improvement over time.

If you use or adapt this Python script, please acknowledge the source and reference the GitHub repository at:
[https://github.com/victoirebuffet/energy_atmospheric_rivers/](https://github.com/victoirebuffet/energy_atmospheric_rivers/)

## Detection Algorithm

The energy atmospheric river (enAR) detection tool (enARDT) developed in this study follows the method of Wille *et al.* (2021) used for polar ARs, which has been later extended to polar aerosol atmospheric rivers in Lapere *et al.* (2024).

The algorithm identifies grid cells in a given area (between 15°S-85°S for Antarctic enARs, and 15°N-85°N for Arctic enARs), where the vertically integrated meridional transport (for vLHT or vSHT schemes) or vertically integrated value (for ILH or ISH schemes) is at or above the Xth (we choose X = 98) monthly percentile, per grid cell, for a given period (here we choose from 1979 to 2023 inclusive). The percentile is derived from 6-hourly vertically integrated meridional transport (both northward and southward) for the same month throughout the whole study period. The 98th percentile used by Wille *et al.* (2021) is thought to be qualitatively better for AR detection, as it avoids identifying features that lack a distinct filament of narrow and intense moisture transport from the subtropics or midlatitudes, which do not fit the AR definition. Additionally, if the algorithm detects a continuous filament of extreme vertically integrated meridional transport that extends at least 20° in the meridional direction, it is classified as an enAR.

## Running the Algorithm

Run this algorithm in two steps:

1. If you wish to create the JSON config file using a Python script, modify the `write_config.py` script according to your needs and then execute this:
    ```sh
    python write_config.py
    ```
    You can skip this step by just creating a `.json` config file with a text editor, in a similar way as the one provided in the main branch.

2. Run the main script:
    ```sh
    python main.py config.json
    ```
