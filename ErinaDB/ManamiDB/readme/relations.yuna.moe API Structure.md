https://raw.githubusercontent.com/BeeeQueue/arm-server/master/README.md

## API

**Base URL:** `https://relations.yuna.moe`

```ts
enum Source {
  anilist,
  anidb,
  myanimelist,
  kitsu,
}
```

### Get IDS:
`GET/POST` `/api/ids`

Either use GET query parameters:
`?source={Source}&id={number}`

or send the query as a POST JSON body:

`{ "anilist": 1337 }`

`[{ "anilist": 1337, "anilist": 69, "anidb": 420 }]`

#### Response

```ts
interface Entry {
  anilist: number | null
  anidb: number | null
  myanimelist: number | null
  kitsu: number | null
}

// { "anilist": 1337 } => Entry | null
// [{ ... }] => Array<Entry | null>
```

**The response code will always be 200 (OK) or 204 (No content).**
If an entry is not found `null` is returned instead.