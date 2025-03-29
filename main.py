import pygame
pygame.init()

from constants.constants import *
from scene_creator import SceneCreator

screen = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption('Image Classifier')
clock = pygame.time.Clock()


def scene_mainloop(scene_creator: SceneCreator, screen: pygame.Surface, clock: pygame.time.Clock):
    scene, command_manager = scene_creator.get_scene_and_manager()

    running = True
    while running:
        command_manager.handle_events()

        screen.fill(SCREEN_FILLING_COLOR)

        scene.draw_elements(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    # from add_folder_scene import AddFolderSceneCreator
    # creator = AddFolderSceneCreator()

    from image_tagging_scene import ImageTaggingSceneCreator
    creator = ImageTaggingSceneCreator('test_scripts/test_images')

    scene_mainloop(creator, screen, clock)
