from typing import Dict
import pandas as pd


def generate_price_matrix(
    offtake_price: pd.Series,
    injection_price: pd.Series=None,
    pv_forecast: pd.Series = None,
    step: int = 100,
    max_p: int = 5000
) -> pd.DataFrame:
    # Create a blank matrix with a column per power step
    columns = list(range(step, max_p + step, step))
    m_blank = pd.DataFrame(index=offtake_price.index, columns=columns)
    
    # Create offtake matrix
    m_price_offtake = m_blank.copy()
    m_price_offtake[step] = offtake_price
    m_price_offtake = m_price_offtake.ffill(axis=1)

    
    if injection_price is not None and pv_forecast is not None:
        # Create injection matrix
        m_price_injection = m_blank.copy()
        m_price_injection[step] = injection_price
        m_price_injection = m_price_injection.ffill(axis=1)
    
        # Create autoconsumption matrix.
        # It expresses the autoconsumption ratio
        autocons = m_blank.copy()
        for column in autocons:
            autocons[column] = (pv_forecast / column).clip(0,1)
        
        
        injection_part = autocons.mul(injection_price, axis=0)
        offtake_part = (1 - autocons).mul(offtake_price, axis=0)
    
        price_matrix = injection_part + offtake_part
    else:
        price_matrix = m_price_offtake
    
    return price_matrix


def map_flexibility_signals(
    matrix: pd.DataFrame,
    mapping: Dict,
    map_negative_values_to=None
) -> pd.DataFrame:
    percentiles = [float(key) for key in mapping]
    signals = matrix.copy()
    
    for column in signals:
        description = signals[column].describe(percentiles=percentiles)

        def signal_mapper(x):
            if map_negative_values_to is not None and x <= 0:
                return map_negative_values_to
            else:
                for percentile in percentiles:
                    if x <= description["{:.0%}".format(percentile)]:
                        return mapping[percentile]
                else:
                    return None
        signals[column] = signals[column].apply(signal_mapper)
        
    return signals