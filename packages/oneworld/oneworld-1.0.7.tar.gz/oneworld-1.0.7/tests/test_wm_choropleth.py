'''Test WebMap choropleth'''
import oneworld as ow
import os

cwd = os.path.dirname(os.path.realpath(__file__))

def test_wm_choro():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    df = ow.load_dataset('farms')
    mymap.add_choropleth(json_file = cwd+'/us_states.json',
                         geoid = 'FIPS', color = 'Land in farms', data = df,
                         json_key = 'GEOID', palette = 'YlOrRd', n_colors = 6)
    mymap.savemap('webmap_choropleth.html')

if __name__ == "__main__":
   test_wm_choro()
