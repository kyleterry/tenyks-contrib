# TenyksScripts Service

This is a service that will run simple scripts. You just need to drop one in
./scripts. They are Python. The scripts should define a `run(data, settings)`
function that takes `data` and `settings` as parameters.

`data` is a dict and contains the payload tenyks sent to services over pub/sub.  
`settings` is a settings object. This is a normal python class, but it acts like
a singleton. All the settings for tenyksscripts are available to the scripts in
./scripts.  

## Example

Lets call the following ./scripts/hello.py:

```python
def run(data, settings):
    if data['payload'] == 'hello':
        return 'world'
```

If someone says "tenyks: hello", this script will return 'world' and that will
show up in the channel.

'nuff said.
