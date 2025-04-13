import argparse
from tools.shortcuts import b

def parse_args(app):
  parser = argparse.ArgumentParser(description='Run the Flask app.')
  parser.add_argument('-r', '--routes', action='store_true', help='Print all routes')
  parser.add_argument('-g', '--grep', type=str, help='Filter routes by group (works with --routes)')
  args = parser.parse_args()

  if args.routes:
      from tools.flasktools import get_routes
      from tabulate import tabulate

      routes = [
          route for route in get_routes(app)
          if not args.grep or any(args.grep in str(value) for value in route.values())
      ]

      print(tabulate(routes, headers="keys", tablefmt="grid"))
      return True
