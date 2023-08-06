import pandas as pd
from src.data_geocoding_utils.shaping_rules import (advanced_city_shaping,
                                     alpha3_to_alpha2_map, basic_city_shaping)


def disambiguate(city_geocode_df, input_city, input_country_code):
    if city_geocode_df.shape[0] == 1:
        return city_geocode_df.iloc[0]

    if len(input_country_code) == 2:
        input_alpha2 = input_country_code
    else:
        input_alpha2 = alpha3_to_alpha2_map[input_country_code]
    unfolded_df = city_geocode_df[['lat', 'lon']].copy(deep=True)

    unfolded_df['geo_point'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].geo_point, axis=1)
    unfolded_df['country_alpha3'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].country_alpha3, axis=1)
    unfolded_df['city'] = city_geocode_df.apply(lambda row: row['CityGeocode'].city, axis=1)
    unfolded_df['postalcode'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].postalcode, axis=1)
    unfolded_df['administrative_level_1'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].administrative_level_1, axis=1)
    unfolded_df['administrative_level_2'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].administrative_level_2, axis=1)
    unfolded_df['country_alpha2'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].country_alpha2, axis=1)
    unfolded_df['source'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].source, axis=1)

    unfolded_df['shaped_city_basic'] = unfolded_df['city'].apply(
        lambda city: basic_city_shaping(city))

    basic_matching_df = unfolded_df[unfolded_df['shaped_city_basic'] == basic_city_shaping(
        input_city)]
    if len(basic_matching_df) == 1:
        return city_geocode_df.loc[basic_matching_df.index].iloc[0]
    unfolded_df['shaped_city_advanced'] = unfolded_df.apply(
        lambda row: advanced_city_shaping(row['city'], row['country_alpha2']), axis=1)

    advanced_matching_df = unfolded_df[unfolded_df['shaped_city_advanced']
                                       == advanced_city_shaping(input_city, input_alpha2)]

    if len(advanced_matching_df) == 1:
        return city_geocode_df.loc[advanced_matching_df.index].iloc[0]

    else:
        return city_geocode_df.iloc[0]
