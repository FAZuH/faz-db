from uuid import UUID

from fazdb.db.fazdb.model import CharacterInfo

from ._common_repository_test import CommonRepositoryTest


class TestCharacterInfoRepository(CommonRepositoryTest.Test[CharacterInfo, int]):

    # override
    def _get_mock_data(self):
        model = self._repo.get_model_cls()

        chuuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
        chuuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
        uuid = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea201").bytes
        mock_data1 = model(character_uuid=chuuid1, uuid=uuid, type='ARCHER')
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.character_uuid = chuuid2
        mock_data4 = mock_data1.clone()
        mock_data4.type = 'ASSASSIN'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "type")

    # override
    @property
    def _repo(self):
        return self.database.character_info_repository
