import markdown


def convert(self, source):
    """
    Аргументы ключевых слов:

    * источник: Исходный текст в виде строки Юникода.

    Обработка уценки происходит в пять этапов:

    1. Куча "препроцессоров" жуют входной текст.
    2. BlockParser() анализирует высокоуровневые структурные элементы
    предварительно обработанного текста в дерево элементов.
    3. Против дерева элементов запускается куча "древовидных процессоров". Один из
    таких treeprocessor запускает InlinePatterns против ElementTree,
    обнаруживая встроенную разметку.
    4. Некоторые постпроцессоры запускаются против текста после дерева элементов
    был сериализован в текст.
    5. Выходные данные записываются в строку.

    """

    # Fixup the source text  # Исправьте исходный текст
    if not source.strip():
        return ''  # a blank unicode string  # пустая строка юникода

    try:
        source = str(source)
    except UnicodeDecodeError as e:  # pragma: no cover  # прагма: без прикрытия

        # Customise error message while maintaining original trackback
        # Настройка сообщения об ошибке при сохранении исходного трекбэка
        e.reason += '. -- Note: Markdown only accepts unicode input!'
        raise

    # Split into lines and run the line preprocessors.
    self.lines = source.split("\n")
    for prep in self.preprocessors:
        self.lines = prep.run(self.lines)

    # Parse the high-level elements.
    root = self.parser.parseDocument(self.lines).getroot()

    # Run the tree-processors
    for treeprocessor in self.treeprocessors:
        newRoot = treeprocessor.run(root)
        if newRoot is not None:
            root = newRoot

    # Serialize _properly_.  Strip top-level tags.
    output = self.serializer(root)
    if self.stripTopLevelTags:
        try:
            start = output.index(
                '<%s>' % self.doc_tag) + len(self.doc_tag) + 2
            end = output.rindex('</%s>' % self.doc_tag)
            output = output[start:end].strip()
        except ValueError as e:  # pragma: no cover
            if output.strip().endswith('<%s />' % self.doc_tag):
                # We have an empty document
                output = ''
            else:
                # We have a serious problem
                raise ValueError('Markdown failed to strip top-level '
                                 'tags. Document=%r' % output.strip()) from e

    # Run the text post-processors
    for pp in self.postprocessors:
        output = pp.run(output)

    return output.strip()