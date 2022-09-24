from typing import Literal, Union
from pydantic import Field
from ldm.dream.app.invocations.image import BaseImageOutput, ImageField
from ldm.dream.app.invocations.baseinvocation import BaseInvocation, InvocationContext


class RestoreFaceInvocation(BaseInvocation):
    """Generates an image using text2img."""
    type: Literal["restore_face"]

    # Inputs
    image: Union[ImageField,None] = Field(description="The input image")
    strength: float               = Field(default=0.75, gt=0, le=1, description="The strength of the restoration")

    class Outputs(BaseImageOutput):
        ...

    def invoke(self, context: InvocationContext) -> Outputs: 
        results = context.generate.upscale_and_reconstruct(
            image_list     = [[self.image.image, 0]],
            upscale        = None,
            strength       = self.strength, # GFPGAN strength
            save_original  = False,
            image_callback = None,
        )

        # Results are image and seed, unwrap for now
        # TODO: can this return multiple results?
        return RestoreFaceInvocation.Outputs.construct(
            image = ImageField(image=results[0][0])
        )
