#include "translation_lookup.h"

#include <QtCore/QSet>

#include <algorithm>

namespace MariTranslation {
namespace {

QString normalizeUncached(QString text) {
    text.replace(QChar(0x00A0), QLatin1Char(' '));
    text.replace(QChar(0x3000), QLatin1Char(' '));
    text.replace(QLatin1Char('\r'), QLatin1Char('\n'));
    text = text.simplified();
    text.remove(QChar(0x200B));
    text.remove(QChar(0x200D));
    text.remove(QChar(0xFEFF));
    while (text.endsWith(QChar(0x2026))) text.chop(1);
    while (text.endsWith(QLatin1String("..."))) text.chop(3);
    if (text.endsWith(QLatin1String(" *"))) text.chop(2);
    text = text.normalized(QString::NormalizationForm_C);
    for (int i = 0; i < text.size(); ++i) {
        const uint code = text.at(i).unicode();
        if (code >= 0xFF01 && code <= 0xFF5E)
            text[i] = QChar(code - 0xFEE0);
    }
    text.replace(QLatin1Char('_'), QLatin1Char(' '));
    text = text.toCaseFolded().normalized(QString::NormalizationForm_D);
    QString stripped;
    stripped.reserve(text.size());
    for (const QChar ch : text) {
        const QChar::Category cat = ch.category();
        if (cat != QChar::Mark_NonSpacing &&
            cat != QChar::Mark_SpacingCombining &&
            cat != QChar::Mark_Enclosing)
            stripped.append(ch);
    }
    stripped.remove(QLatin1Char(' '));
    return stripped.normalized(QString::NormalizationForm_C);
}

QString normalizeForPaint(const QString &text) {
    // Dictionary indexing bypasses this cache. A per-thread cache avoids a
    // lock in painting and remains useful after thousands of entries load.
    thread_local QHash<QString, QString> cache;
    static constexpr int kCacheLimit = 4096;
    const auto cached = cache.constFind(text);
    if (cached != cache.constEnd()) return cached.value();
    const QString result = normalizeUncached(text);
    if (cache.size() >= kCacheLimit) cache.clear();
    cache.insert(text, result);
    return result;
}

} // namespace

void Lookup::add(const QString &source, const QString &translated) {
    if (!source.isEmpty() && !translated.isEmpty())
        exact_.insert(source, translated);
}

void Lookup::rebuild() {
    normalized_.clear();
    sortedKeys_.clear();
    QSet<QString> ambiguous;
    for (auto it = exact_.cbegin(); it != exact_.cend(); ++it) {
        const QString key = normalizeUncached(it.key());
        const auto existing = normalized_.constFind(key);
        if (existing != normalized_.constEnd() && existing.value() != it.value())
            ambiguous.insert(key);
        else if (existing == normalized_.constEnd())
            normalized_.insert(key, it.value());
    }
    // Ambiguous spellings still resolve exactly. Never guess from QHash order.
    for (const QString &key : ambiguous) normalized_.remove(key);

    sortedKeys_.reserve(exact_.size());
    for (auto it = exact_.cbegin(); it != exact_.cend(); ++it)
        sortedKeys_.push_back(qMakePair(it.key().toCaseFolded(), it.key()));
    std::sort(sortedKeys_.begin(), sortedKeys_.end(),
              [](const QPair<QString, QString> &a,
                 const QPair<QString, QString> &b) {
                  return a.first == b.first ? a.second < b.second : a.first < b.first;
              });
}

QString Lookup::findElided(const QString &text) const {
    QString base = text;
    base.chop(text.endsWith(QChar(0x2026)) ? 1 : 3);
    base = base.trimmed();
    if (base.size() < 2) return {};
    const QString low = base.toCaseFolded();
    auto it = std::lower_bound(
        sortedKeys_.begin(), sortedKeys_.end(), low,
        [](const QPair<QString, QString> &entry, const QString &value) {
            return entry.first < value;
        });
    QString best;
    for (; it != sortedKeys_.end() && it->first.startsWith(low); ++it) {
        const QString &source = it->second;
        if (best.isEmpty() || source.size() < best.size() ||
            (source.size() == best.size() && source < best))
            best = source;
    }
    return best.isEmpty() ? QString() : exact_.value(best);
}

QString Lookup::find(const QString &text) const {
    const QString trimmed = text.trimmed();
    if (trimmed.isEmpty()) return {};

    const auto exact = exact_.constFind(trimmed);
    if (exact != exact_.constEnd()) return exact.value();

    QString key = trimmed;
    QString stateSuffix;
    if (key.endsWith(QLatin1Char('*'))) {
        key.chop(1);
        key = key.trimmed();
        stateSuffix = QStringLiteral("*");
    }
    if (key.contains(QLatin1Char('&')))
        key.remove(QLatin1Char('&'));
    const auto mnemonic = exact_.constFind(key);
    if (mnemonic != exact_.constEnd()) return mnemonic.value() + stateSuffix;

    const auto normalized = normalized_.constFind(normalizeForPaint(key));
    if (normalized != normalized_.constEnd())
        return normalized.value() + stateSuffix;

    if (key.endsWith(QChar(0x2026)) || key.endsWith(QLatin1String("..."))) {
        const QString elided = findElided(key);
        if (!elided.isEmpty()) return elided + stateSuffix;
    }
    return {};
}

} // namespace MariTranslation
