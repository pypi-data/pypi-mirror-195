# BASH completion script for pdm
# Generated by pycomplete 0.3.2

_pdm_25182a7ef85b840e_complete()
{
    local cur script coms opts com
    COMPREPLY=()
    _get_comp_words_by_ref -n : cur words

    # for an alias, get the real script behind it
    if [[ $(type -t ${words[0]}) == "alias" ]]; then
        script=$(alias ${words[0]} | sed -E "s/alias ${words[0]}='(.*)'/\\1/")
    else
        script=${words[0]}
    fi

    # lookup for command
    for word in ${words[@]:1}; do
        if [[ $word != -* ]]; then
            com=$word
            break
        fi
    done

    # completing for an option
    if [[ ${cur} == --* ]] ; then
        opts="--config --help --ignore-python --pep582 --verbose --version"

        case "$com" in

            (add)
            opts="--dev --dry-run --editable --global --group --help --lockfile --no-editable --no-isolation --no-self --no-sync --prerelease --project --save-compatible --save-exact --save-minimum --save-wildcard --skip --unconstrained --update-all --update-eager --update-reuse --verbose"
            ;;

            (build)
            opts="--config-setting --dest --help --no-clean --no-isolation --no-sdist --no-wheel --project --skip --verbose"
            ;;

            (cache)
            opts="--help --verbose"
            ;;

            (completion)
            opts="--help"
            ;;

            (config)
            opts="--delete --global --help --local --project --verbose"
            ;;

            (export)
            opts="--dev --format --global --group --help --lockfile --no-default --output --production --project --pyproject --verbose --without-hashes"
            ;;

            (import)
            opts="--dev --format --global --group --help --project --verbose"
            ;;

            (info)
            opts="--env --global --help --packages --project --python --verbose --where"
            ;;

            (init)
            opts="--global --help --non-interactive --project --python --skip --verbose"
            ;;

            (install)
            opts="--check --dev --dry-run --global --group --help --lockfile --no-default --no-editable --no-isolation --no-lock --no-self --production --project --skip --verbose"
            ;;

            (list)
            opts="--csv --exclude --fields --freeze --global --graph --help --include --json --markdown --project --resolve --reverse --sort --verbose"
            ;;

            (lock)
            opts="--check --global --help --lockfile --no-isolation --project --refresh --skip --verbose"
            ;;

            (plugin)
            opts="--help --verbose"
            ;;

            (publish)
            opts="--ca-certs --comment --help --identity --no-build --password --project --repository --sign --skip --username --verbose"
            ;;

            (remove)
            opts="--dev --dry-run --global --group --help --lockfile --no-editable --no-isolation --no-self --no-sync --project --skip --verbose"
            ;;

            (run)
            opts="--global --help --list --project --site-packages --skip --verbose"
            ;;

            (search)
            opts="--help --verbose"
            ;;

            (self)
            opts="--help --verbose"
            ;;

            (show)
            opts="--global --help --keywords --license --name --platform --project --summary --verbose --version"
            ;;

            (sync)
            opts="--clean --dev --dry-run --global --group --help --lockfile --no-default --no-editable --no-isolation --no-self --only-keep --production --project --reinstall --skip --verbose"
            ;;

            (update)
            opts="--dev --global --group --help --lockfile --no-default --no-editable --no-isolation --no-self --no-sync --outdated --prerelease --production --project --save-compatible --save-exact --save-minimum --save-wildcard --skip --top --unconstrained --update-all --update-eager --update-reuse --verbose"
            ;;

            (use)
            opts="--first --global --help --ignore-remembered --project --skip --verbose"
            ;;

            (venv)
            opts="--help"
            ;;

        esac

        COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
        __ltrim_colon_completions "$cur"

        return 0;
    fi

    # completing for a command
    if [[ $cur == $com ]]; then
        coms="add build cache completion config export import info init install list lock plugin publish remove run search self show sync update use venv"

        COMPREPLY=($(compgen -W "${coms}" -- ${cur}))
        __ltrim_colon_completions "$cur"

        return 0
    fi
}

complete -o default -F _pdm_25182a7ef85b840e_complete pdm
