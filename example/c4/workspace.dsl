workspace "Personal AI Trainer" "Example design package for the interview-to-design method." {

    model {
        athlete = person "Athlete" "States a goal, logs completed workouts, reads plans."

        llm = softwareSystem "LLM Provider" "Drafts plan content from a goal and training history." "External"

        trainer = softwareSystem "Personal AI Trainer" "Turns a stated goal into a training plan and adapts it to the workouts actually completed." {

            planApi = container "Plan API" "Generates and serves TrainingPlans." "Python, FastAPI"
            adaptation = container "Adaptation Engine" "Adapts a plan from Sessions and Metrics." "Python"
            db = container "Database" "PostgreSQL" "PostgreSQL 16" "Database"

            planApi -> db "Reads and writes plan data" "SQL"
            planApi -> adaptation "Triggers recalculation" "In-process"
            adaptation -> db "Rewrites remaining weeks" "SQL"
        }

        athlete -> planApi "Submits goals, logs Sessions" "HTTPS, JSON"
        planApi -> llm "Requests a draft plan" "HTTPS, JSON"
    }

    views {
        systemContext trainer "Context" "The trainer among its actor and the external provider." {
            include *
            autolayout lr 300 300
        }

        container trainer "Containers" "The deployable pieces inside the trainer." {
            include *
            autolayout lr 350 300
        }

    }
}
