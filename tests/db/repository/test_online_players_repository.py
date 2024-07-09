from uuid import UUID

from fazdb.db.fazdb.model import OnlinePlayers

from ._common_repository_test import CommonRepositoryTest


class TestOnlinePlayersRepository(CommonRepositoryTest.Test[OnlinePlayers, int]):

    # override
    def _get_mock_data(self):
        model = self._repo.get_model_cls()

        uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
        uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
        mock_data1 = model(uuid=uuid1, server='a')
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.uuid = uuid2
        mock_data4 = mock_data1.clone()
        mock_data4.server = 'b'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "server")

    # override
    @property
    def _repo(self):
        return self.database.online_players_repository
