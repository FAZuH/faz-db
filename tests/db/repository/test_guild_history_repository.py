from fazdb.db.fazdb.model import GuildHistory

from ._common_repository_test import CommonRepositoryTest


class TestGuildHistoryRepository(CommonRepositoryTest.Test[GuildHistory, int]):

    # override
    def _get_mock_data(self):
        model = self._repo.get_model_cls()

        mock_data1 = model(
            name="a", level=1.0, territories=1, wars=1, member_total=1,
            online_members=1, datetime=self._get_mock_datetime()
        )
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        del mock_data3.unique_id
        mock_data3.name = "b"
        mock_data3 = mock_data3.clone()
        mock_data4 = mock_data1.clone()
        mock_data4.level = 2.0
        return (mock_data1, mock_data2, mock_data3, mock_data4, "level")

    # override
    @property
    def _repo(self):
        return self.database.guild_history_repository
