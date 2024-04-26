# Incorporate Changes to Casual-to-Annual Trips Ratio

In order to account for changes in annual and casual member ridership, make the following changes

1. At end of `eda_temporal.ipynb`
   - in **User Behaviour Insights**
     - add the following in a sub-section
       ### Show Ratio of Monthly Casual to Annual Ridership
       ```python
       %%time
       query = f"""
               WITH t1 AS (
                   -- get monthly departures (trips) by each type of member
                   SELECT started_at_year AS year,
                          started_at_month AS month,
                          REPLACE(user_type, ' Member', '') AS user_type,
                          COUNT(DISTINCT(trip_id)) AS trips
                   FROM read_parquet({fpaths_proc_all})
                   GROUP BY all
               )
               t2 AS (
                   PIVOT t1
                   ON user_type
                   USING SUM(trips)
               )
               SELECT *,
                      Casual/Annual AS ratio
               FROM t2
               """
       df_monthly_casual_to_annual = run_sql_query(query).convert_dtypes()
       pu.show_df(df_monthly_casual_to_annual)
       ```
       Show above as a chart and add **Observations**
     - add the following in a sub-section
       ### Show Ratio of Casual to Annual Ridership on Weekdays and Weekends per Month
       ```python
       %%time
       query = f"""
               WITH t1 AS (
                   -- get monthly departures (trips) by each type of member
                   SELECT started_at_year AS year,
                          started_at_month AS month,
                          (
                            CASE
                                WHEN ISODOW(started_at)-1 IN (5, 6)
                                THEN 'Weekend'
                                ELSE 'Weekday'
                            END
                          ) AS day_of_week,
                          REPLACE(user_type, ' Member', '') AS user_type,
                          COUNT(DISTINCT(trip_id)) AS trips
                   FROM read_parquet({fpaths_proc_all})
                   GROUP BY all
               )
               t2 AS (
                   PIVOT t1
                   ON user_type || '_' || day_of_week
                   USING SUM(trips)
               ),
               t3 AS (
                    SELECT *,
                           Casual_Weekday/Annual_Weekday AS ratio_weekday,
                           Casual_Weekend/Annual_Weekend AS ratio_weekend
                    FROM t2
               ),
               t4 AS (
                   UNPIVOT (
                       SELECT year,
                              month,
                              ratio_weekday,
                              ratio_weekend
                       FROM t3
                   )
                   ON
                   INTO
                       NAME variable
                       VALUE value
               )
               SELECT * EXCLUDE(variable),
                      REPLACE(variable, 'ratio_', '') AS variable
               FROM t4
               """
       df_monthly_casual_to_annual_dow = run_sql_query(query).convert_dtypes()
       pu.show_df(df_monthly_casual_to_annual_dow)
       ```
       Show above as a chart and add **Observations**
   - before the **Recommendations** section, add a new section **Export to Disk** with a single sub-section (**Ratio of Monthly Casual-to-Annual Ridership**) and export monthly casual to annual ratio (`df_monthly_casual_to_annual`) in a `casual_to_annual_ridership_ratio__*.parquet.gzip` file
     ```python
     %%time
     fname_prefix = "casual_to_annual_ridership_ratio"
     _ = df_monthly_casual_to_annual.pipe(
         flut.load,
         processed_data_dir,
         fname_prefix,
         my_timezone,
         True,
     )
     ```
   - modify `df_temporal_recommends` as follows
     - change `weekday_prime` to `weekday_prime_casual_dominant`
       - no changes
     - add `weekday_prime_annual_dominant`
       - same as `weekday_prime_casual_dominant`
     - change `weekend_prime` to `weekend_prime_casual_dominant`
       - no changes
     - add `weekend_prime_annual_dominant`
       - [contains](https://stackoverflow.com/a/46399979/4057186) `AND FALSE` in order to avoid making any selection
     - change `weekday_offseason` to `weekday_offseason_casual_dominant`
       - no changes
     - add `weekday_offseason_annual_dominant`
       - same as `weekday_offseason_casual_dominant`
2. In `generate_recommendations.ipynb`
   - get filepath to file with ratio of casual to annual ridership
     ```python
     # ratio of trips by casual to annual members
     fpath_recommends_temporal = glob(
         os.path.join(processed_data_dir, 'casual_to_annual_ridership_ratio__*.parquet.gzip')
     )[0]
     ```
   - Add a section **Get Casual-to-Annual Ridership Ratio** containing the following
     ```python
     df_ctoa = pd.read_parquet()
     latest_month_ctoa_ratio = df_ctoa.sort_values(by=['year_month'])['ratio'].squeeze()

     if latest_month_ctoa_ratio > 0.4:
         weekday_prime = 'weekday_prime_casual_dominant'
         weekend_prime = 'weekend_prime_casual_dominant'
         weekday_offseason = 'weekday_offseason_casual_dominant
     else:
         weekday_prime = 'weekday_prime_annual_dominant'
         weekend_prime = 'weekend_prime_annual_dominant'
         weekday_offseason = 'weekday_offseason_annual_dominant'
     ```
   - In **Transform** > **Get Recommended Schedule**, change the following
     - `recommended_hour_filters['weekday_prime']` to `recommended_hour_filters[weekday_prime]`
     - `recommended_hour_filters['weekend_prime']` to `recommended_hour_filters[weekend_prime]`
     - `recommended_hour_filters['weekday_offseason']` to `recommended_hour_filters[weekday_offseason]`
