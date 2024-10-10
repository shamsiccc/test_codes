import pytest
import requests


class TestYandexDisk:
    def setup_method(self):
        self.headers = {
            'Authorization': 'OAuth y0_AgAAAAAzDHljAAyXCgAAAAET9dO5AAAhbijy3TdOPYPBVVujmutTZ_rDug'
        }
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.folder_name = 'test_folder'

        self.delete_test_folder()

    def delete_test_folder(self):
        try:
            response = requests.delete(f'{self.base_url}?path={self.folder_name}', headers=self.headers)
            if response.status_code not in [200, 404]:
                print(f'Error while deleting test folder: {response.content}')
        except Exception as e:
            print(f'Error while deleting test folder: {e}')

    def test_check_folder_existence(self):
        response = requests.get(f'{self.base_url}?path={self.folder_name}', headers=self.headers)

        if response.status_code == 200:
            print("Папка существует.")
        elif response.status_code == 404:
            print("Папка не существует.")
        else:
            print(f"Ошибка при проверке существования папки: {response.status_code}")

    @pytest.mark.parametrize(
        'key,value,statuscode',
        [
            ['path', 'folder', 400],
            ['path', 'folder', 201],
            ['path', 'folder', 409],
        ]
    )
    def test_create_folder(self, key, value, statuscode):

        self.test_check_folder_existence()

        params = {key: value}
        response = requests.put(self.base_url, headers=self.headers, params=params)

        assert response.status_code == statuscode