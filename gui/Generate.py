#Attribution:

import torch
#from tqdm.auto import tqdm
import tqdm
import cuda
print("CUDA_V", cuda.__version__)

#import point_e
from point_e.diffusion.configs import DIFFUSION_CONFIGS, diffusion_from_config
from point_e.diffusion.sampler import PointCloudSampler
from point_e.models.download import load_checkpoint
from point_e.models.configs import MODEL_CONFIGS, model_from_config
from point_e.util.plotting import plot_point_cloud

import urllib.request

#NOTES: Bear in mind:
#--> the __init__.py of point-e was changed.
#--> the file plotting.py of \point-e\point_e\util\plotting.py was changed.
#--> the file \point-e\point_e\models\transformer.py was changed.
#--> the file \point-e\point_e\models\download.py

import openai

# from gui.Generate import DALL_E
# from gui.Generate import Chat_GPT
# from gui.Generate import Point_E


class Chat_GPT():
    def __init__(self):
        self.model = "gpt-3.5-turbo" #gpt-4
        self._return = None

    def Generate(self, prompt, text_only=True):
        # openai.ChatCompletion.create()
        GPT_Completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "%s" % prompt}])
        self._return = GPT_Completion
        return self._return.get('choices')[0]['message']['content'] if text_only else self._return



class DALL_E():
    def __init__(self):
        self.response = None
        self.image = None
        self.url = None
        self.image_counter = -1

    def Generate(self, prompt = "a white siamese cat", image_only=True):
        self.response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        self.image = self.response['data'][0]
        self.url = self.response['data'][0]['url']

        print("Image downloaded and saved successfully!")
        self.image_counter += 1
        return urllib.request.urlretrieve(self.url, r"./resources/intermediary_path/" + "DALL-E_SAVE_%s.png" % self.image_counter)[0] if image_only else self.response


class Point_E():
    def __init__(self):
        print("Version", torch.version.cuda)
        #print("Cuda", torch.)#.cuda_is_available())
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print("self.device", self.device)

        print('creating base model...')
        self.base_name = 'base40M-textvec'
        self.base_model = model_from_config(MODEL_CONFIGS[self.base_name], self.device)
        self.base_model.eval()
        self.base_diffusion = diffusion_from_config(DIFFUSION_CONFIGS[self.base_name])

        print('creating upsample model...')
        self.upsampler_model = model_from_config(MODEL_CONFIGS['upsample'], self.device)
        self.upsampler_model.eval()
        self.upsampler_diffusion = diffusion_from_config(DIFFUSION_CONFIGS['upsample'])

        print('downloading base checkpoint...')
        self.base_model.load_state_dict(load_checkpoint(self.base_name, self.device))

        print('downloading upsampler checkpoint...')
        self.upsampler_model.load_state_dict(load_checkpoint('upsample', self.device))
        self.sampler = PointCloudSampler(
            device=self.device,
            models=[self.base_model, self.upsampler_model],
            diffusions=[self.base_diffusion, self.upsampler_diffusion],
            num_points=[1024, 4096 - 1024],   #[1024, 4096 - 1024],
            aux_channels=['R', 'G', 'B'],
            guidance_scale=[3.0, 0.0],
            model_kwargs_key_filter=('texts', ''), # Do not condition the upsampler at all
    )
    def Generate(self, sampler=None, prompt = 'a red motorcycle', plot=False, coords_only=True):
        # Set a prompt to condition on.
        sampler = self.sampler if sampler is None else sampler
        # Produce a sample from the model.
        samples = None
        for x in tqdm.tqdm(sampler.sample_batch_progressive(batch_size=1, model_kwargs=dict(texts=[prompt]))):
            samples = x
        pc = sampler.output_to_point_clouds(samples)[0]
        fig = plot_point_cloud(pc, grid_size=3, fixed_bounds=((-0.75, -0.75, -0.75),(0.75, 0.75, 0.75))) \
            if plot is True else None
        print("PC", pc, type(pc))
        return pc.coords if coords_only is True else pc

# ass_cloud = Point_E()
# fuck_ass_cloud= ass_cloud.Generate()
# fuck_ass_cloud.save()
#fuck_ass_cloud.write_ply()