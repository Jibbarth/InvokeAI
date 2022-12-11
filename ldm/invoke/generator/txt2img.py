'''
ldm.invoke.generator.txt2img inherits from ldm.invoke.generator
'''
import PIL.Image
import torch

from .base import Generator
from .diffusers_pipeline import StableDiffusionGeneratorPipeline


class Txt2Img(Generator):
    def __init__(self, model, precision):
        super().__init__(model, precision)

    @torch.no_grad()
    def get_make_image(self,prompt,sampler,steps,cfg_scale,ddim_eta,
                       conditioning,width,height,step_callback=None,threshold=0.0,perlin=0.0,
                       attention_maps_callback=None,
                       **kwargs):
        """
        Returns a function returning an image derived from the prompt and the initial image
        Return value depends on the seed at the time you call it
        kwargs are 'width' and 'height'
        """
        self.perlin = perlin
        uc, c, extra_conditioning_info   = conditioning

        # noinspection PyTypeChecker
        pipeline: StableDiffusionGeneratorPipeline = self.model
        pipeline.scheduler = sampler

        def make_image(x_T) -> PIL.Image.Image:
            pipeline_output = pipeline.image_from_embeddings(
                latents=x_T,
                num_inference_steps=steps,
                text_embeddings=c,
                unconditioned_embeddings=uc,
                guidance_scale=cfg_scale,
                callback=step_callback,
                extra_conditioning_info=extra_conditioning_info,
                # TODO: eta = ddim_eta,
                # TODO: threshold = threshold,
                # FIXME: Attention Maps Callback merged from main, but not hooked up
                #     in diffusers branch yet. - keturn
                # attention_maps_callback      = attention_maps_callback,
            )

            return pipeline.numpy_to_pil(pipeline_output.images)[0]

        return make_image


    # returns a tensor filled with random numbers from a normal distribution
    def get_noise(self,width,height):
        device         = self.model.device
        if self.use_mps_noise or device.type == 'mps':
            x = torch.randn([1,
                                self.latent_channels,
                                height // self.downsampling_factor,
                                width  // self.downsampling_factor],
                               device='cpu').to(device)
        else:
            x = torch.randn([1,
                                self.latent_channels,
                                height // self.downsampling_factor,
                                width  // self.downsampling_factor],
                               device=device)
        if self.perlin > 0.0:
            x = (1-self.perlin)*x + self.perlin*self.get_perlin_noise(width  // self.downsampling_factor, height // self.downsampling_factor)
        return x

