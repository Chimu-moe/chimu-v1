from chimu.shared.utils.digit import isDigit
import datadog

from chimu.v1.error_codes import ERR_CODE_BEATMAP_NOT_FOUND, ERR_CODE_INT_ERROR, Error, Success
from chimu.shared.utils.mysql import GetDatabaseConnection
from starlette.requests import Request


async def get_map(request: Request):
    datadog.statsd.increment('chimu.api.v1.get_map',
                             tags=["version:1", "application:web"])

    map_id = request.path_params['map_id']
    if not isDigit(map_id):
        return Error(401, ERR_CODE_INT_ERROR, f'Error: map_id is not an int!')
    map_id = int(map_id)

    with GetDatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Beatmaps WHERE BeatmapId = ? LIMIT 1', (map_id,))

        for bm in cursor:
            return Success(
                {
                    'BeatmapId': bm[0],
                    'ParentSetId': bm[1],
                    'DiffName': bm[2],
                    'FileMD5': bm[3],
                    'Mode': bm[4],
                    'BPM': bm[5],
                    'AR': bm[6],
                    'OD': bm[7],
                    'CS': bm[8],
                    'HP': bm[9],
                    'TotalLength': bm[10],
                    'HitLength': bm[11],
                    'Playcount': bm[12],
                    'Passcount': bm[13],
                    'MaxCombo': bm[14],
                    'DifficultyRating': bm[15],
                    'OsuFile': bm[16],
                    'DownloadPath': f'/d/{bm[1]}'
                }
            )

    return Error(404, ERR_CODE_BEATMAP_NOT_FOUND, 'Error: Beatmap not found!')
