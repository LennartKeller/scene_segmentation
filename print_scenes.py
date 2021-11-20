import click
import json

def newline():
    return "\n"

@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option('--span', is_flag=True, help="Show span indices in original text too.")
def print_scenes(filename, span):
    """Print scenes"""
    with open(filename) as f:
        data = json.load(f)
    text = data["text"]
    scenes = data["scenes"]
    output = "\n\n".join([
        f"Type: {scene['type']} {str(scene.copy()) + newline() if span else newline()}{text[scene['begin']:scene['end']]}"
        for scene in scenes
        ])
    click.echo(output)

if __name__ == "__main__":
    print_scenes()
