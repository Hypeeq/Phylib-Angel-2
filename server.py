import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import Physics
import math

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = self.path.split('?')[0]
        if parsed_path == '/':
            self.send_response(302)
            self.send_header('Location', '/shoot.html')
            self.end_headers()
        elif parsed_path == '/shoot.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('shoot.html', 'rb') as file:
                self.wfile.write(file.read())
        elif parsed_path.startswith('/table-'):
            table_number = parsed_path.split('-')[1]  # Extracting table number from URL
            table_path = f"table-{table_number}.svg"  # Constructing filename dynamically
            if os.path.exists(table_path):
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                with open(table_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes("404 Not Found: %s does not exist" % parsed_path, 'utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("404 Not Found: %s" % parsed_path, 'utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode('utf-8'))

        if self.path == '/display.html':
            # Delete all table-?.svg files in the server’s directory
            for filename in os.listdir():
                if filename.startswith('table-') and filename.endswith('.svg'):
                    os.remove(filename)

            # Extract parameters from the form data
            sb_number = int(post_params['sb_number'][0])
            sb_x = float(post_params['sb_x'][0])
            sb_y = float(post_params['sb_y'][0])
            rb_x = float(post_params['rb_x'][0])
            rb_y = float(post_params['rb_y'][0])
            rb_dx = float(post_params['rb_dx'][0])
            rb_dy = float(post_params['rb_dy'][0])

            # Compute the speed of the rolling ball
            speed_rb = math.sqrt(rb_dx ** 2 + rb_dy ** 2)

            # Compute acceleration with drag
            if speed_rb > Physics.VEL_EPSILON:
                acceleration_x = -rb_dx / speed_rb * Physics.DRAG
                acceleration_y = -rb_dy / speed_rb * Physics.DRAG
            else:
                acceleration_x = 0.0
                acceleration_y = 0.0

            # Construct a Table and add the Balls
            table = Physics.Table()
            still_ball = Physics.StillBall(sb_number, Physics.Coordinate(sb_x, sb_y))
            rolling_ball = Physics.RollingBall(0, Physics.Coordinate(rb_x, rb_y), Physics.Coordinate(rb_dx, rb_dy), Physics.Coordinate(acceleration_x, acceleration_y))
            table += still_ball
            table += rolling_ball

            # Save the table-?.svg files and segment the table
            file_index = 0
            while table is not None:
                # Write the SVG representation to a file
                with open(f"table-{file_index}.svg", "w") as svg_file:
                    svg_content = table.svg()
                    svg_file.write(svg_content)
                
                # Continue simulation
                table = table.segment()
                file_index += 1

            # Generate HTML response
            html_response = "<html><body><h1>Original Ball Positions and Velocities</h1>"
            html_response += "<ul>"
            html_response += f"<li>Still Ball: ({sb_x}, {sb_y})</li>"
            html_response += f"<li>Rolling Ball Position: ({rb_x}, {rb_y})  Velocity: ({rb_dx}, {rb_dy})</li>"
            for file_index in range(file_index):
                with open(f"table-{file_index}.svg", "rb") as svg_file:
                    svg_content = svg_file.read().decode('utf-8')
                    html_response += f"<div>{svg_content}</div>"

            html_response += "<a href='/shoot.html'>Back</a>"
            html_response += "</body></html>"


            # Send HTML response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(html_response, 'utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("404 Not Found: %s" % self.path, 'utf-8'))



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number")
        sys.exit(1)

    httpd = HTTPServer(('localhost', port), MyHandler)
    print("Server listening on port:", port)
    httpd.serve_forever()
