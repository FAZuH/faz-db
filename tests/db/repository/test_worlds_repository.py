from datetime import datetime

from fazdb.db.fazdb.model import Worlds

from ._common_repository_test import CommonRepositoryTest


class TestWorldsRepository(CommonRepositoryTest.Test[Worlds, int]):

    # override
    def _get_mock_data(self):
        model = self._repo.get_model_cls()

        mock_data1 = model(name="WC1", player_count=50, time_created=datetime.now().replace(microsecond=0))
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.name = "WC2"
        mock_data4 = mock_data1.clone()
        mock_data4.player_count = 49
        mock_data4.time_created = datetime.now().replace(microsecond=0)
        return (mock_data1, mock_data2, mock_data3, mock_data4, "player_count")

    # override
    @property
    def _repo(self):
        return self.database.worlds_repository
