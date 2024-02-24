# Flat Districts Visualization

## Overview
This project aims to visualize the distribution of rental flats in Dortmund with their respective rents per square meter. 
It uses web scraping techniques to gather flat listings from the wg-gesucht website. 
The data is then visualized on a heatmap overlaid on a map of Dortmund, providing insights into the rental market across different districts.

## Technologies Used
- **Beautiful Soup**: library for parsing data
- **Folium**: library for creating interactive maps 
- **Google Maps Geocoding API**: used to convert addresses into geographic coordinates 

## How to Run
1. Clone the repository to your local machine.
2. Obtain a Google Maps API key and update the `GOOGLE_MAPS_API_KEY` variable in `secretsKeys.py` with your key.
3. Run the `main.py` script to fetch flat listings, geocode locations, and generate the heatmap.
    ```bash
    python main.py
    ```
4. The heatmap visualization will be saved as `dortmund_heatmap.html` in the project directory.
