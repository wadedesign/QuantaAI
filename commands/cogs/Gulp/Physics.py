import pymunk
import nextcord
import matplotlib.pyplot as plt
from nextcord import Embed
from nextcord.ext import commands


"""
Using PyMunk to simulate physics
"""

class PhysicsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.space = pymunk.Space()
        self.space.gravity = (0, -1000)  # Set the gravity

    @commands.command()
    async def simulate(self, ctx):
        """Start the physics simulation"""
        # Create a ground body
        ground = pymunk.Body(body_type=pymunk.Body.STATIC)
        ground.position = (400, 50)
        ground_shape = pymunk.Segment(ground, (-400, -50), (400, -50), 10)
        self.space.add(ground, ground_shape)

        # Create a dynamic body
        body = pymunk.Body(mass=1, moment=10)
        body.position = (200, 200)
        shape = pymunk.Circle(body, radius=20)
        self.space.add(body, shape)

        # Lists to store positions for plotting
        x_positions = []
        y_positions = []

        # Run the simulation
        for _ in range(100):
            self.space.step(0.02)  # Step the simulation

            # Store body positions
            for body in self.space.bodies:
                position = body.position
                x_positions.append(position.x)
                y_positions.append(position.y)

        # Plot the positions
        plt.plot(x_positions, y_positions)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Simulation State")

        # Save the plot as an image file
        image_path = "simulation_state.png"
        plt.savefig(image_path)

        # Close the plot
        plt.close()

        # Create the embedded message
        embed = Embed(title="Simulation State")
        for body in self.space.bodies:
            position = body.position
            embed.add_field(name=f"Body: {body}", value=f"Position: {position}", inline=False)
        embed.set_image(url=f"attachment://{image_path}")

        # Send the message with the embedded image
        with open(image_path, "rb") as file:
            picture = nextcord.File(file, filename=image_path)
            await ctx.send(file=picture, embed=embed)

def setup(bot):
    bot.add_cog(PhysicsCog(bot))


