# Check Redirects

Check Redirects is a web application used to expose the true path taken between the URL you enter and its final destination.

## Usage

Check Redirects is primarily a web application. To access it, browse to [https://check-redirects.com](https://check-redirects.com). 

However, you can query the endpoint to retrieve the answer.

`curl 'https://check-redirects.com/api/v1/redirect/checker' -d '{"url":"amzn.to"}'`

It expects only one argument; `url`. 

## Installation

To install locally please read [DEV-README.md](https://github.com/danielmichaels/check-redirects.com/blob/master/DEV-README.md)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
