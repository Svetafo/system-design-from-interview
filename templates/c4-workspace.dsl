workspace "[System]" "[What the system is for, one sentence.]" {

    model {
        user = person "[Actor]" "[Who they are and what they want.]"
        ext  = softwareSystem "[External system]" "[What it provides.]" "External"

        sys = softwareSystem "[System]" "[What it does.]" {
            api = container "[API]" "[What this container serves.]" "[Language, framework]"
            db  = container "[Database]" "[What it stores.]" "PostgreSQL 16" "Database"
        }

        user -> api "[What the actor does]" "HTTPS, JSON"
        api  -> db  "Reads and writes [entities]" "SQL"
        api  -> ext "[What it asks for]" "HTTPS, JSON"
    }

    views {
        systemContext sys "Context" "[Who is involved and what sits outside.]" {
            include *
            autolayout lr 300 300
        }
        container sys "Containers" "[The deployable pieces inside.]" {
            include *
            autolayout lr 350 300
        }
    }
}

// Container and external system names come from glossary.md and are used verbatim.
// The default export is C4-PlantUML, which applies the canonical C4 palette and ignores
// styles declared here, so none are declared. Render:
//   bash tools/c4-render.sh <workspace.dsl> <output-dir>
