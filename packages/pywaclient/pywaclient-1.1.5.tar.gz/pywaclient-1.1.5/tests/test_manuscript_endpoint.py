#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from init_client import world_id, client

if __name__ == '__main__':
    manuscripts = client.world.manuscripts(world_id)
    for manuscript in manuscripts:
        client.manuscript.delete(manuscript['id'])

    test_manuscript_1 = client.manuscript.put(
        {
            'title': 'Test Manuscript Creation',
            'world': {
                'id': world_id}
        }
    )
    test_manuscript_2 = client.manuscript.put(
        {
            'title': 'Test Manuscript Creation 2',
            'world': {
                'id': world_id}
        }
    )
    response_patch_manuscript_2 = client.manuscript.patch(
        test_manuscript_2['id'],
        {
            'excerpt': 'This is an excerpt for an manuscript.'
        }
    )

    full_test_manuscript_2 = client.manuscript.get(
        test_manuscript_2['id'],
        2
    )

    assert full_test_manuscript_2['excerpt'] == 'This is an excerpt for an manuscript.'

    client.manuscript.delete(test_manuscript_1['id'])
    client.manuscript.delete(test_manuscript_2['id'])
