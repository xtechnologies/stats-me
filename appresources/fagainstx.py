import matplotlib.pyplot as plt

plt.style.use('dark_background')


class fagainstx:
    def __init__(self, x_axis:list, y_axis:list):
        self.x_axis = x_axis
        self.y_axis = y_axis
        
    def plot(self):
        # Create a bar chart
        plt.bar(self.x_axis, self.y_axis)

        # Adding labels and title
        plt.xlabel('Value of X')
        plt.ylabel('Frequency')
        plt.title('Bar Chart of frequency against x')

        # Display the chart
        plt.show()