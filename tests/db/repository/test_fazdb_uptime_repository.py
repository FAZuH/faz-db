from fazdb.db.fazdb.model import FazdbUptime

from ._common_repository_test import CommonRepositoryTest


class TestFazdbUptimeRepository(CommonRepositoryTest.Test[FazdbUptime, int]):

    # override
    def _get_mock_data(self):
        model = self._repo.get_model_cls()

        mock_data1 = model(
            start_time=self._get_mock_datetime().replace(day=1),
            stop_time=self._get_mock_datetime().replace(day=2)
        )
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.start_time = self._get_mock_datetime().replace(day=3, microsecond=0)
        mock_data4 = mock_data1.clone()
        mock_data4.stop_time = self._get_mock_datetime().replace(day=3, microsecond=0)
        return (mock_data1, mock_data2, mock_data3, mock_data4, "stop_time")

    # override
    @property
    def _repo(self):
        return self.database.fazdb_uptime_repository
