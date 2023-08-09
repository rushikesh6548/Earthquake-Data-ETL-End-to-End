# Earthquake Data Pipeline Project

This project demonstrates building a data pipeline for processing earthquake data from the USGC API occurred between 2010-2023. The pipeline consists of four main steps:

1. Data Extraction: Data is obtained from the USGC API for earthquakes occurred between 2010-2023.
2. Data Transformation: Raw data is stored in Google Cloud Storage and ETL code is written using MAGE AI to transform it into a more useful form.
3. Data Modeling: Data is normalized into Fact and Dimension tables following a Star Schema to optimize it for querying and analysis.
4. Data Loading: Data is loaded into BigQuery using a loader code and a dashboard is created using Looker Studio for visualization and exploration.

## Architecture Diagram

![Architecture Diagram](insert_image_link_here)

## MAGE AI Data Pipeline : 
![image](https://user-images.githubusercontent.com/46419407/236880606-898b9a56-f064-4f82-8042-810593b6fc75.png)

## Dashboard can be found here : 
https://lookerstudio.google.com/reporting/63fa702f-a50f-4deb-bc4b-df938d470de0

![image](https://github.com/rushikesh6548/Earthquake-Data-ETL-End-to-End/assets/46419407/08de62da-8dc4-4c12-baea-b5ef6fd3fa04)


## Project Steps:

1. Creating a Google Cloud Storage bucket and update the `config.yml` on MAGE AI file with the bucket name and credentials.
2. Settin up Google Compute Instances and installing MAGE AI on the instance and starting the service to make it hear on required port .
3. Extraction data from Google Cloud Storage into MAGE AI loader 
4. Transforming our data according to our Data Model 
5. Set up a BigQuery table with the schema for the fact and dimension tables.
6. Loading our data into Google Big Query by providing necessary credentials like table name , dataset name . 
7. The data is loaded into google bigquery . We Create Dashboard using 

## Data Schema

The data is modeled using a Star Schema with the following fact and dimension tables:

- **Fact Table**
  - earthquake_id
  - datetime_id
  - location_id
  - magnitude_id
  - depth
  - nst
  - gap
  - dmin
  - rms
  

- **Datetime Dim table : datetime_dim**
   - earthquake_datetime
    - earthquake_hour
    - hour
    - earthquake_day
    - earthquake_weekday
    - earthquake_month
    - earthquake_year
    
  - **Datetime Dim table : magnitude_dim**
    - earthquake_mag
    - magnitude_id
    - magnitude_err
    - magnitude_nst
  
- **Location Dim table : location_dim**
  - location_id
  - longitude
  - latitude_id
  - place
  - location_source 

## Building Dashboard on Tableau Desktop : 
1. Data transformation - Denormalizing
   ![image](https://github.com/rushikesh6548/Earthquake-Data-ETL-End-to-End/assets/46419407/ed7adaea-66bf-44f4-a1ee-9634df8623cf)


## Conclusion

We created a ETL Pipeline with our ETL code on MAGE AI and used Google Compute Instance to run MAGE AI . Loaded the transformed data to Google Big Query and Made Dashboard on 
Google LookUpStudio.
