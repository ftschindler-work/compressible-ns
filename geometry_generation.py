import numpy as np


def segment(data, kind, d_spatial, number, previous_number, b_marker, *args):
    # Writing the to define segments in the outcoming file "data" with:
    # kind: The shape of the geometric
    # d_spatial: Spatial discretization
    # number: Order of the segment
    # previous_number: Number of segments defined before
    # b_marker: Number of the boundary marker
    # *args: Other attributes, depending of the geometric shape (like width and length for a chamber)

    data.write("#\n# List the segments by index, start and end node, and boundary marker.\n#\n# Segment " + str(number)
               + "\n")
    size = 0

    # Calculate the size/ number of segments depending of the shape of the geometric
    if(kind == "chamber"):
        size = int(2 * (args[0] + args[1]) / d_spatial)
    else:
        if(kind == "circle"):
            size = int(360 / d_spatial)
        else:
            print("Please use a known geometric shape!")
            data.close()
            exit()

    # Write the indices of the segments
    for i in range(previous_number + 1, size + previous_number):
        x = i
        y = i + 1
        data.write(str(i) + "   " + str(x) + "   " + str(y) + "   " + str(b_marker) + "\n")
    data.write(str(size + previous_number) + "   " + str(size + previous_number) + "   " + str(previous_number + 1) +
               "   " + str(b_marker) + "\n")

    # Return the size, to know the written number of segments
    return size


def circle(data, r, d_angular, x_init, y_init, b_marker, previous_number):
    # Calculate and write the nodes for a circle in the outcoming file: data
    # r: Radius of the circle
    # d_angular: Discretization of the d_angular
    # x_init: X-Position of the center of the circle
    # y_init: Y-Position of the center of the circle
    # b_marker: Number of the boundary marker
    # previous_number: Number of the written nodes before

    # Test, if the angular discretization allows an uniform discretization at 360°
    if(360 / d_angular % 1 != 0):
        print("The angular discretization does not fit")
        data.close()
        exit()

    # Calculate the number of nodes of the circle
    size = int(360 / d_angular)

    # Calculate and write the Positions of the nodes of the circle
    for i in range(size):
        x = np.sin(np.deg2rad(i * d_angular)) * r
        y = np.cos(np.deg2rad(i * d_angular)) * r
        data.write(str(i + 1 + previous_number) + "\t" + "{0:.4f}".format(x + x_init) + "\t" +
                   "{0:.4f}".format(y + y_init) + "\t" + str(b_marker) + "\n")


def rectangle(data, width, length, d_spatial, x_init, y_init, b_marker, previous_number):
    # Calculate and write the nodes for a chamber in the outcoming file: data
    # width: Width of the chamber
    # length: Length of the chamber
    # d_spatial: Spatial discretization of the chamber
    # x_init: X-Position of the lower left corner of the chamber
    # y_init: Y-Position of the lower left corner of the chamber
    # b_marker: Number of the boundary marker
    # previous_number: Number of the written nodes before

    # Calculating of the number of the nodes of the chamber
    size = int(2 * (width + length) / d_spatial)

    # Test, if the spatial discretization allows an uniform discretization
    if(width / d_spatial % 1 != 0 or length / d_spatial % 1 != 0):
        print("The discretization with the width " + width + ", length" + length + "and discretization" + d_spatial +
              "does not fit!")
        data.close()
        exit()

    # Calculate and write the position of the nodes
    for i in range(int(size)):

        # Calculate the nodes on the left side of the rectangle
        if(i < width / d_spatial + 1):
            x = 0
            y = i * d_spatial
        else:

            # Calculate the nodes on the upper side of the rectangle
            if(i < (length + width) / d_spatial + 1):
                x = i * d_spatial - width
                y = width
            else:

                # Calculate the nodes on the right side of the rectangle
                if(i < (2 * width + length) / d_spatial + 1):
                    x = length
                    y = width - (i * d_spatial - width - length)
                else:

                    # Calculate the nodes on the lower side of the rectangle
                    x = length - (i * d_spatial - 2 * width - length)
                    y = 0
        data.write(str(i + 1 + previous_number) + "\t" + "{0:.4f}".format(x + x_init) + "\t" +
                   "{0:.4f}".format(y + y_init) + "\t" + str(b_marker) + "\n")


if __name__ == '__main__':

    # Declaration of the attributes of the geometric shapes
    width_1 = 3
    width_2 = 1
    length_1 = 5
    length_2 = 1
    radius = 0.2
    d_spatial_1 = 0.2
    d_spatial_2 = 1
    d_angular_1 = 3

    # Calculation of the number of nodes (=size) of every geometric shape
    size_1 = int(2 * (width_1 + length_1) / d_spatial_1)
    size_2 = int(2 * (width_2 + length_2) / d_spatial_2)
    size_3 = int(360 / d_angular_1)
    size_total = size_1 + size_2 + size_3

    # Introduction of the outcoming file
    description = "#\n"
    data_out = open("test.poly", "w")
    data_out.write(description+"# Declare "+str(size_total) +
            " vertices, 2 dimensions, 0 attributes, 1 boundary marker\n" + "#\n" + str(int(size_total)) +
            " 2 0 1\n" + "#\n# List the vertices by index, x, y, and boundary marker.\n#\n")

    # Calculating of the nodes of the outer rectangle
    data_out.write("# Points of the outer rectangle\n#\n")
    rectangle(data_out, width_1, length_1, d_spatial_1, 0, 0, 0, 0)

    # Calculating of the nodes of the inner rectangle(=particle)
    data_out.write("#\n#Points of the inner rectangle\n#\n")
    rectangle(data_out, width_2, length_2, d_spatial_2, 1, 1, 0, size_1)

    # Exemplary calculation of another particle(here circle)
    data_out.write("#\n# Points of the inner Circle\n#\n")
    circle(data_out, r=radius, d_angular=d_angular_1, x_init=3.5, y_init=1.5, b_marker=1, previous_number=size_1+size_2)

    # Defining of the segments of all nodes
    data_out.write("#\n# Declare the number of segments and the number of boundary markers.\n#\n " + str(size_total) +
                   " 1" + "\n")
    help = segment(data_out, "chamber", d_spatial_1, 1, 0, 1, width_1, length_1)
    help += segment(data_out, "chamber", d_spatial_2, 2, help, 2, width_2, length_2)
    segment(data_out, "circle", d_angular_1, 3, help, 3)

    # Defining of holes
    data_out.write("#\n# Declare the number of holes.\n#\n 2\n#\n# Define a hole by giving the coordinates of" +
                   " one point inside it."
                   + "\n 1 \t" + "{0:.4f}".format(1 + length_2 / 2) + "\t" + "{0:.4f}".format(1 + width_2 / 2) + "\n" +
                   "2\t" + "{0:.4f}".format(3.5) + "\t" + "{0:.4}".format(1.5))
    data_out.close()
