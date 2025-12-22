/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly ALLOWED_HOSTS?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

