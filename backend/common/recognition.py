import logging

from common.features import featurize_file


logger = logging.getLogger(__name__)


def recognize_saved_file(path, prediction_service):
    """
    Recognize chords in the specified audio file.

    Parameters
    ----------
    path : str
        A path to the saved audio file.
    prediction_service : PredictionService
        A service used to make chord name predictions.

    Returns
    -------
    list
        A list of dictionaries, each with the keys: {'timeOffset', 'name', 'confidence'}.
    """
    logger.info(f'Starting recognition of: "{path}"')
    exclude_columns = ['time_offset', 'is_silent']
    df_features = featurize_file(path)
    logger.info(f'Featurized data shape: {df_features.shape}')

    # Prepare dataset for predictions. This involves removing features we use for internal purposes.
    df_features_not_silent = df_features[~df_features['is_silent']]
    df_features_pred = df_features_not_silent.drop(columns=exclude_columns)
    logger.info(f'Non-silent data shape: {df_features_not_silent.shape}')

    # Request predictions.
    df_predictions = prediction_service.predict(df_features_pred)

    # Attach some of the information we removed earlier.
    df_predictions['time_offset'] = df_features_not_silent.reset_index(drop=True)['time_offset']

    # Final smoothing and postprocessing.
    logger.info('Postprocessing started')
    result = df_predictions.rename(columns={'time_offset': 'timeOffset'}).to_dict(orient='records')
    result = remove_repeating_chords(result)
    logger.info('Postprocessing finished')

    return result


def remove_repeating_chords(chords):
    """
    Post-process the recognized chords, replacing identical adjacent chords with a single one.

    Parameters
    ----------
    chords : list
        List of recognized chords from `recognize_saved_file`

    Returns
    -------
    list
        A list in the identical format as the input list but with duplicates removed.
    """
    result = []
    prev_chord = None
    for chord in chords:
        if chord['name'] != prev_chord:
            result.append(chord)
            prev_chord = chord['name']
    return result
